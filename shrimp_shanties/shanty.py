import json
import csv
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Pattern:
    start: int
    end: int
    pattern: str


class Beat:
    """ The class for containing patterns about a beat and deciding when to emit a note """

    def __init__(self, path: Path):
        try:
            with open(path / 'info.json') as f:
                info = json.load(f)
                self.name = info['name']
                self.video_audio = info.get('video_audio')
                self.audio_name = info.get('audio_name')
                self.background = info.get('background')
                self.patterns = info['patterns']

            with open(path / 'index.csv') as f:
                self.patterns = []
                r = csv.reader(f)
                for row in r:
                    self.patterns.append(Pattern(int(row[0]), int(row[1]), row[2]))
        except Exception as e:
            raise BeatLoadError(e)


class BeatLoadError(Exception):
    def __init__(self, e):
        self._e = e

    def __str__(self):
        return f'BeatLoadError({self._e})'
