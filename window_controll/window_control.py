import time
from typing import Union

import pyautogui as pya
import win32gui

from config import Config


def set_window_position(window_id: int) -> None:
    win32gui.SetForegroundWindow(window_id)
    win32gui.MoveWindow(
        window_id,
        Config.config()["WindowConfig"].getint("start_x"),
        Config.config()["WindowConfig"].getint("start_y"),
        Config.config()["WindowConfig"].getint("width"),
        Config.config()["WindowConfig"].getint("height"),
        True,
    )


def click(x: int, y: int) -> None:
    pya.moveTo(x=x, y=y, duration=0.0)
    pya.click(x=x, y=y)


def scroll(x: int, y: int, scroll_amount: Union[int, float]) -> None:
    pya.moveTo(x=x, y=y, duration=0.0)
    pya.scroll(scroll_amount, x=x, y=y)


def page_down():
    pya.press("pagedown")
    # sleep for correct bufferization
    time.sleep(1.0)
