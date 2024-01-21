from pathlib import Path

from pytheme.cli import main

if __name__ == "__main__":
    fp = Path(__file__).parent.joinpath("test_config.json")
    main(config_fp=fp)
