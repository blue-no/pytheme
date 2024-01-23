import json
from datetime import datetime, timedelta
from pathlib import Path

from pytheme.schedule import run_scheduling
from pytheme.utils import read_config

t = datetime.now()
tmnus1 = (t - timedelta(minutes=1)).strftime("%H:%M")
tplus1 = (t + timedelta(minutes=1)).strftime("%H:%M")
tplus2 = (t + timedelta(minutes=2)).strftime("%H:%M")
tplus3 = (t + timedelta(minutes=3)).strftime("%H:%M")

config_dict = {
    "themes": [
        {
            "name": "theme1",
            "mode": "light",
            "wp": "C:\\Windows\\Web\\Wallpaper\\ThemeB\\img24.jpg",
        },
        {
            "name": "theme2",
            "mode": "dark",
            "wp": "C:\\Windows\\Web\\Wallpaper\\ThemeB\\img25.jpg",
        },
        {
            "name": "theme3",
            "mode": "light",
            "wp": "C:\\Windows\\Web\\Wallpaper\\ThemeB\\img26.jpg",
        },
        {
            "name": "theme4",
            "mode": "dark",
            "wp": "C:\\Windows\\Web\\Wallpaper\\ThemeB\\img27.jpg",
        },
    ],
    "schedule": [
        {"time": tmnus1, "theme": "theme1", "confirm": False},
        {"time": tplus1, "theme": "theme2", "confirm": True},
        {"time": tplus2, "theme": "theme3", "confirm": False},
        {"time": tplus3, "theme": "theme4", "confirm": True},
    ],
    "application_delay": 3.0,
    "ask_interval_mins": 0.4,
}

config_fp = Path("./tests/test_config.json")
with config_fp.open("w") as f:
    json.dump(config_dict, f, indent=2)

run_scheduling(config=read_config(config_fp))
