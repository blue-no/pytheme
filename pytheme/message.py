from __future__ import annotations

import ctypes
from contextlib import contextmanager
from tkinter import Tk, messagebox
from typing import Any, Generator


class Message:
    def __init__(self) -> None:
        self._appname = "PyTheme"
        ctypes.windll.shcore.SetProcessDpiAwareness(True)

    @contextmanager
    def _messagebox_setup(self) -> Generator[Tk, Any, Any]:
        root = Tk()
        root.withdraw()
        root.attributes("-topmost", True)
        try:
            yield root
        finally:
            root.destroy()

    def show_error(self, message: str) -> None:
        with self._messagebox_setup():
            messagebox.showerror(title=self._appname, message=message)

    def show_info(self, message: str) -> None:
        with self._messagebox_setup():
            messagebox.showinfo(title=self._appname, message=message)

    def ask_ifyes(self, message: str) -> bool:
        with self._messagebox_setup():
            return messagebox.askyesno(title=self._appname, message=message)
