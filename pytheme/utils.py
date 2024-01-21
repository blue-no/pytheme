from __future__ import annotations

import json
from datetime import datetime, time
from pathlib import Path
from typing import Any


def read_config(fp: Path) -> dict[str, Any]:
    with fp.open("r", encoding="utf-8") as f:
        d = json.load(f)
    return d


def _str_to_time(time_str: str) -> time:
    return datetime.strptime(time_str, "%H:%M").time()
