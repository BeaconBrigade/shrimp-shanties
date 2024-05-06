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
- `patterns` Array, where each item has the following keys:
  - `name` Name of the pattern
  - `beats_at` Array of beat numbers where a note should be played
    (relative to the first beat of the pattern is repeated)

## Properties of `index.csv`

Defines using beat ranges where each pattern is used. 

Columns:
- `start` The starting beat (inclusive)
- `end` The ending beat (exclusive)
- `pattern` The name of the pattern to be used over this range
