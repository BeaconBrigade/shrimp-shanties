import csv
import json
from dataclasses import dataclass

from shrimp_shanties.asset_manager import AssetManager
from shrimp_shanties.game.rhythm.note import Shrimp


@dataclass
class Pattern:
    length: int
    name: str


class Shanty:
    """ The class for containing patterns about a beat and deciding when to emit a note """

    def __init__(self, path):
        self.file_name = path
        path = AssetManager.load_shanty(path)
        try:
            with open(path / 'info.json') as f:
                info = json.load(f)
                self.name = info['name']
                self.video_audio = info.get('video_audio')
                self.audio_name = info.get('audio_name')
                self.background = info.get('background')
                patterns = info['patterns']
                self.patterns = dict()
                for name, value in patterns.items():
                    self.patterns[name] = dict()
                    self.patterns[name]["len"] = value["len"]
                    for k, v in list(value.items())[1:]:
                        self.patterns[name][int(k)] = v

            with open(path / 'index.csv') as f:
                self.index = []
                r = csv.reader(f)
                # skip headers
                for row in r:
                    try:
                        self.index.append(Pattern(int(row[0]), row[1]))
                    except:
                        pass
        except Exception as e:
            raise BeatLoadError(e)

    def note(self, beat):
        # find which pattern we're in
        num = 0
        for p in self.index:
            if beat in range(num, num + p.length):
                pat = p
                break
            num += p.length
        else:
            raise SongOver()

        # find offset into pattern
        pat_info = self.patterns[pat.name]
        offset = beat % pat_info["len"]

        # return note from pattern
        d = pat_info.get(offset)
        if d is not None:
            return Shrimp(int(d))
        return None

    def length(self):
        return sum(x.length for x in self.index)

    def __str__(self):
        return f"Shanty(name='{self.name}', va={self.video_audio}, an={self.audio_name}, b={self.background}, " + \
            f"p={self.patterns}, index={self.index})"


class BeatLoadError(Exception):
    def __init__(self, e):
        self._e = e

    def __str__(self):
        return f'BeatLoadError({self._e})'


class SongOver(Exception):
    pass
