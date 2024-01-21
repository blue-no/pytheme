from pathlib import Path

from .cli import main

if __name__ == "__main__":
    fp = Path(__file__).parent.joinpath("config.json")
    main(config_fp=fp)
