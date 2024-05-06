import os
from pathlib import Path

if __name__ == '__main__':
    game_dir = Path(__file__).parent / 'shrimp_shanties'
    os.chdir(game_dir)

    from shrimp_shanties import main

    main()
