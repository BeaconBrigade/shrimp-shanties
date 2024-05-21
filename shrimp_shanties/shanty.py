import json
import csv
from dataclasses import dataclass

from shrimp_shanties.asset_manager import AssetManager
from shrimp_shanties.game.rhythm.note import Shrimp


@dataclass
class Pattern:
    start: int
    end: int
    name: str

    def __contains__(self, item: int):
        return item in range(self.start, self.end)


class Shanty:
    """ The class for containing patterns about a beat and deciding when to emit a note """

    def __init__(self, path):
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
                next(r)
                for row in r:
                    self.index.append(Pattern(int(row[0]), int(row[1]), row[2]))
        except Exception as e:
            raise BeatLoadError(e)

    def note(self, beat):
        # find which pattern we're in
        for p in self.index:
            if beat in p:
                pat = p
                break
        else:
            raise Exception("beat not in shanty")

        # find offset into pattern
        pat_info = self.patterns[pat.name]
        offset = beat % pat_info["len"]

        # return note from pattern
        d = pat_info.get(offset)
        if d is not None:
            return Shrimp(int(d))
        return None

    def __str__(self):
        return f"Shanty(name='{self.name}', va={self.video_audio}, an={self.audio_name}, b={self.background}, " + \
            f"p={self.patterns}, index={self.index})"


class BeatLoadError(Exception):
    def __init__(self, e):
        self._e = e

    def __str__(self):
        return f'BeatLoadError({self._e})'
