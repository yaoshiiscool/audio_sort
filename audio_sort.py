import argparse
import librosa
import numpy as np
import soundfile as sf
import subprocess
import os

def main():
    parser = argparse.ArgumentParser(description="Sort audio segments by average amplitude (RMS)")
    parser.add_argument("input_file", help="Path to input MP3 file")
    parser.add_argument("output_file", help="Path to output MP3 file")
    parser.add_argument("--segments", type=int, default=10, help="Number of segments to divide the audio into (default: 10)")
    args = parser.parse_args()

    # Load the audio file
    try:
        y, sr = librosa.load(args.input_file, sr=None)  # sr=None to preserve original sample rate
    except Exception as e:
        print(f"Error loading audio file: {e}")
        return

    # Calculate segment length
    total_samples = len(y)
    seg_len = total_samples // args.segments

    # Divide into segments
    segments = []
    for i in range(args.segments):
        start = i * seg_len
        end = (i + 1) * seg_len if i < args.segments - 1 else total_samples
        segments.append(y[start:end])

    # Sort segments by RMS (average amplitude)
    segments.sort(key=lambda s: np.sqrt(np.mean(s**2)))

    # Concatenate sorted segments
    combined = np.concatenate(segments)

    # Write to temporary WAV file
    temp_wav = 'temp_audio.wav'
    try:
        sf.write(temp_wav, combined, sr)
    except Exception as e:
        print(f"Error writing temporary WAV file: {e}")
        return

    # Convert to MP3 using ffmpeg
    try:
        subprocess.run(['ffmpeg', '-i', temp_wav, '-y', args.output_file], check=True)
        print(f"Processed audio saved to {args.output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error converting to MP3: {e}")
    except FileNotFoundError:
        print("Error: ffmpeg not found. Please install ffmpeg to export MP3 files.")
    finally:
        # Clean up temporary file
        if os.path.exists(temp_wav):
            os.remove(temp_wav)

if __name__ == "__main__":
    main()