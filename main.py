import os
import sys
from pathlib import Path


if __name__ == '__main__':
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        game_dir = Path(sys._MEIPASS) / 'shrimp_shanties'
    else:
        game_dir = Path(__file__).parent / 'shrimp_shanties'

    os.chdir(game_dir)

    from shrimp_shanties import main

    main()
