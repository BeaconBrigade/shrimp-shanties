# Beats: `.shanty` files

These beats contain the information for each song. They contain meta
information, audio file locations, beat patterns and the timing for
each note.

## Terminology and Information

*Beat* - A frame in the game where a *note* could be played. There are
60 per second.

*Note* - When the player has to input a key of the correct direction.

## Properties of `info.json`

Meta information about the beat.

- `name` Name of the specific beat
- `video_audio` Location of an mp4 file which contains video for the
background and the audio of the song
- `audio_name` Location of the mp3 file which just contains audio
- `background` Location of an mp4 or png which is the background
for the song.
- `patterns` Object keyed by names of a pattern and values are objects keyed by:
  - `len` is the length of the pattern in beats
  - Beat numbers where a note should be played (relative to the
  first beat of the pattern is repeated) mapping to the direction a
  note should face (0, 1, 2, 3) = (up, right, down, left)
    

## Properties of `index.csv`

Defines using beat ranges where each pattern is used. 

Columns:
- `len` The length in beats this pattern should be used for
- `pattern` The name of the pattern to be used
