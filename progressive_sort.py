import argparse
import librosa
import numpy as np
import soundfile as sf
import subprocess
import os

def main():
    parser = argparse.ArgumentParser(description="Create a progressive sorted audio file")
    parser.add_argument("input_file", help="Path to input MP3 file")
    parser.add_argument("output_file", help="Path to output MP3 file")
    args = parser.parse_args()

    # Load the audio file
    try:
        y, sr = librosa.load(args.input_file, sr=None)  # Preserve original sample rate
    except Exception as e:
        print(f"Error loading audio file: {e}")
        return

    total_samples = len(y)
    print(f"Loaded audio: {total_samples} samples at {sr} Hz")

    # Calculate 1 ms in samples
    one_ms_samples = int(sr / 1000)
    if one_ms_samples < 1:
        one_ms_samples = 1

    # List to hold all versions
    all_versions = []

    k = 1
    while True:
        segment_len = total_samples // k
        if segment_len < one_ms_samples:
            break

        print(f"Processing with {k} segments (segment length: {segment_len} samples)")

        if k == 1:
            # Original song
            combined = y
        else:
            # Divide into k segments
            segments = []
            for i in range(k):
                start = i * segment_len
                end = (i + 1) * segment_len if i < k - 1 else total_samples
                segments.append(y[start:end])

            # Sort segments by RMS
            segments.sort(key=lambda s: np.sqrt(np.mean(s**2)))

            # Concatenate
            combined = np.concatenate(segments)

        all_versions.append(combined)
        k *= 2

    # Concatenate all versions
    final_combined = np.concatenate(all_versions)
    print(f"Final combined audio: {len(final_combined)} samples")

    # Write to temporary WAV file
    temp_wav = 'temp_progressive.wav'
    try:
        sf.write(temp_wav, final_combined, sr)
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