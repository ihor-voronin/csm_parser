import logging
from typing import Any, Dict, List

import win32gui

from settings import Settings


def winEnumHandler(hwnd: Any, all_windows: List[Dict[Any, Any]]) -> None:
    if win32gui.IsWindowVisible(hwnd):
        window_name = win32gui.GetWindowText(hwnd)
        if window_name:
            all_windows.append({hwnd: window_name})


def get_window_id_from_opened_windows() -> int:
    all_windows: list = []
    win32gui.EnumWindows(winEnumHandler, all_windows)
    window_name = Settings.window_name.lower()
    for all_windows_dict in all_windows:
        for key, value in all_windows_dict.items():
            if window_name in value.lower():
                logging.info(f"Window with name '{window_name}' found with id {key}")
                return key
    raise Exception(f"window {window_name} not found")
