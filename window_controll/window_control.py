import time
from typing import Union

import pyautogui as pya
import win32com.client
import win32con
import win32gui

from settings import Settings


def set_window_position(window_id: int) -> None:
    print(
        f"Set window to position ({Settings.start_coordinate_x}, {Settings.start_coordinate_y})"
    )
    print(f"Set window resolution {Settings.window_width} X {Settings.window_height}")
    win32gui.MoveWindow(
        window_id,
        Settings.start_coordinate_x,
        Settings.start_coordinate_y,
        Settings.window_width,
        Settings.window_height,
        True,
    )
    shell = win32com.client.Dispatch("WScript.Shell")
    shell.SendKeys("%")
    win32gui.SetForegroundWindow(window_id)
    time.sleep(1.0)


def click(x: int, y: int) -> None:
    pya.moveTo(x=x, y=y, duration=0.0)
    pya.click(x=x, y=y)


def scroll(x: int, y: int, scroll_amount: Union[int, float]) -> None:
    pya.moveTo(x=x, y=y, duration=0.0)
    pya.scroll(scroll_amount, x=x, y=y)


def page_down() -> None:
    pya.press("pagedown")
    # sleep for correct bufferization
    time.sleep(1.0)


def minimize_window(window_id: int) -> None:
    time.sleep(1.0)
    win32gui.ShowWindow(window_id, win32con.SW_MINIMIZE)


def maximize_window(window_id: int) -> None:
    time.sleep(1.0)
    win32gui.ShowWindow(window_id, win32con.SW_MAXIMIZE)
