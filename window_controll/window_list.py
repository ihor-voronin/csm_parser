from typing import Any

import win32gui


def winEnumHandler(hwnd: Any, ctx: Any) -> None:
    if win32gui.IsWindowVisible(hwnd):
        window_name = win32gui.GetWindowText(hwnd)
        if window_name:
            print(f"{hwnd:10} -- {window_name}")


def list_of_open_windows() -> None:
    print("window_id \t window_name")
    return win32gui.EnumWindows(winEnumHandler, None)
