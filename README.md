# audio_sort 
Programs that literally sort samples of audio via the amplitude of their respective samples. 

1. `audio_sort.py`: Takes an MP3 file, divides it into a specified number of segments, sorts by amplitude, and outputs a new MP3.
2. `progressive_sort.py`: Creates a long MP3 that concatenates the original song followed by versions divided into increasing numbers of segments (powers of 2) and sorted by amplitude, up to segments of 1 ms length.

##Requirements 
See requirements.txt

##Usage
'''bash
python audio_sort.py <input_file.mp3> <output_file.mp3> [--segments N]
python progressive_sort.py <input_file.mp3> <output_file.mp3>
'''

Example usage:
'''bash
python audio_sort.py song.mp3 sorted_song.mp3 --segments 20
python progressive_sort.py input.mp3 output.mp3
'''

Made for MADD 26210 Media Arts and Design, taught by Takashi Shallow. 
