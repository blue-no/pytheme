from __future__ import annotations

import ctypes
import winreg
from dataclasses import dataclass
from enum import Enum
from pathlib import Path


def parse_themes(theme_list: list[dict]) -> dict[str, Theme]:
    theme_dict: dict[str, Theme] = {}
    for th in theme_list:
        mode_ = th.get("mode", None)
        wp_ = th.get("wp", None)
        theme_dict[th["name"]] = Theme(
            name=th["name"],
            mode=ColorMode(mode_) if mode_ is not None else None,
            wp=Path(wp_) if wp_ is not None else None,
        )
    return theme_dict


@dataclass
class Theme:
    name: str
    mode: ColorMode | None = None
    wp: Path | None = None


class ColorMode(Enum):
    DARK = "dark"
    LIGHT = "light"

    @staticmethod
    def opposite(mode: ColorMode) -> ColorMode:
        if mode == ColorMode.DARK:
            return ColorMode.LIGHT
        elif mode == ColorMode.LIGHT:
            return ColorMode.DARK
        else:
            raise NotImplementedError


class Personalization:
    _REG_KEY_PATH = (
        "SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize"
    )
    _REG_VAL_NAMES = [
        "AppsUseLightTheme",
        "SystemUsesLightTheme",
    ]

    def apply_colormode(self, mode: ColorMode) -> None:
        if mode == ColorMode.DARK:
            val = 0
        elif mode == ColorMode.LIGHT:
            val = 1
        else:
            raise NotImplementedError

        with winreg.OpenKeyEx(
            winreg.HKEY_CURRENT_USER,
            self._REG_KEY_PATH,
            access=winreg.KEY_WRITE,
        ) as key:
            for name in self._REG_VAL_NAMES:
                winreg.SetValueEx(key, name, 0, winreg.REG_DWORD, val)

    def apply_wallpaper(self, wp: Path) -> None:
        if not wp.exists():
            return
        ctypes.windll.user32.SystemParametersInfoW(
            20,
            0,
            wp.absolute().as_posix(),
            0,
        )
