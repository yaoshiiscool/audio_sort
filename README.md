# Audio Segment Sorter

This directory contains two Python programs for audio processing:

1. `audio_sort.py`: Takes an MP3 file, divides it into a specified number of segments, sorts by amplitude, and outputs a new MP3.
2. `progressive_sort.py`: Creates a long MP3 that concatenates the original song followed by versions divided into increasing numbers of segments (powers of 2) and sorted by amplitude, up to segments of 1 ms length.

## Requirements

- Python 3.x
- librosa library
- soundfile library
- FFmpeg (required for MP3 export)

### Installing Dependencies

1. Install Python packages:
   ```bash
   pip install -r requirements.txt
   ```

2. Install FFmpeg:
   - On macOS: `brew install ffmpeg`
   - On Ubuntu/Debian: `sudo apt install ffmpeg`
   - On Windows: Download from https://ffmpeg.org/download.html

## Usage

### audio_sort.py

```bash
python audio_sort.py <input_file.mp3> <output_file.mp3> [--segments N]
```

- `input_file.mp3`: Path to the input MP3 file
- `output_file.mp3`: Path where the output MP3 file will be saved
- `--segments N`: Optional. Number of segments to divide the audio into (default: 10)

### progressive_sort.py

```bash
python progressive_sort.py <input_file.mp3> <output_file.mp3>
```

- `input_file.mp3`: Path to the input MP3 file
- `output_file.mp3`: Path where the output MP3 file will be saved

This creates a very long MP3 file containing:
- The original song
- The song divided into 2 segments and sorted by amplitude
- The song divided into 4 segments and sorted
- And so on, doubling the number of segments each time, until segment length reaches approximately 1 ms

## Example usage

```bash
python audio_sort.py song.mp3 sorted_song.mp3 --segments 20
python progressive_sort.py input.mp3 output.mp3
```

## How it works

1. The program loads the input MP3 file using librosa.
2. It calculates the length of each segment by dividing the total audio length by the number of segments.
3. Each segment is analyzed for its RMS value, which represents the average amplitude.
4. The segments are sorted in ascending order of RMS (quietest to loudest).
5. The sorted segments are concatenated into a single audio file.
6. The result is exported as a new MP3 file.

Made for MADD 26210 Media Arts and Design, taught by Takashi Shallow.
