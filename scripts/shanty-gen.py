import argparse
import csv
import json
import os
import pathlib
import random


def main():
    parser = argparse.ArgumentParser(prog="shanty-gen", description="Generates a random shanty.", epilog="wassaa")
    parser.add_argument("name", help="name of the shanty (.shanty extension is added automatically)")
    parser.add_argument("-l", "--len", help="length of the song in beats", default=10000)
    parser.add_argument("--mp4", help="mp4 containing video and audio for the shanty", default="")
    parser.add_argument("--mp3", help="mp3 containing audio for the shanty", default="")
    parser.add_argument("--png", help="png containing the background for the shanty", default="")
    args = parser.parse_args()

    info = INFO_TEMPLATE
    info["name"] = args.name
    info["video_audio"] = args.mp4
    info["audio_name"] = args.mp3
    info["background"] = args.png

    length = int(args.len)
    if length < 60 or length > 216000:
        print("Invalid length: ensure length is between 60 and 216000 beats")
        return

    work_dir = SHANTY_DIR / f"{args.name}.shanty"
    os.mkdir(work_dir)
    with open(work_dir / "info.json", 'w') as f:
        json.dump(info, f)

    with open(work_dir / "index.csv", 'w', newline="") as f:
        header = ("len", "pattern")
        count = 0

        w = csv.writer(f)
        w.writerow(header)

        while count < int(args.len):
            next_len = random.randrange(30, 240)
            next_pat = random.choice(list(info["patterns"].keys()))
            w.writerow((next_len, next_pat))
            count += next_len


SHANTY_DIR = pathlib.Path(__file__).parent.parent / "assets" / "shanties"

INFO_TEMPLATE = {
    "name": "NAME",
    "video_audio": "VIDEO_AUDIO",
    "audio_name": "AUDIO_NAME",
    "background": "BACKGROUND",
    "patterns":
        {
            "joe": {"len": 120, "60": 0, "90": 2, "100": 1},
            "jan": {"len": 120, "60": 1, "90": 2, "100": 3},
            "bil": {"len": 20, "5": 3},
            "jak": {"len": 20, "5": 2},
            "mat": {"len": 20, "5": 1},
            "noa": {"len": 20, "5": 0},
            "test-1-nps": {"len": 90, "0": 0},
            "hang": {"len": 60},

            "stair": {"len": 60, "0": 0, "15": 1, "30": 2, "45": 3},
            "estair": {"len": 60, "0": 0, "15": 1, "30": 2},
            "bwstair": {"len": 60, "0": 3, "15": 2, "30": 1, "45": 0},
            "ebwstair": {"len": 60, "0": 3, "15": 2, "30": 1},

            "hstair": {"len": 30, "0": 3, "15": 2},
            "shstair": {"len": 30, "0": 1, "15": 0},

            "hbwstair": {"len": 30, "0": 2, "15": 3},
            "shbwstair": {"len": 30, "0": 0, "15": 1},
            "line": {"len": 30, "0": [0, 1, 2, 3]}
        }
}

if __name__ == "__main__":
    main()
