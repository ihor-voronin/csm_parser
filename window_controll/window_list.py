from typing import Any, Dict, List

import win32gui


def winEnumHandler(hwnd: Any, all_windows: List[Dict[Any, Any]]) -> None:
    if win32gui.IsWindowVisible(hwnd):
        window_name = win32gui.GetWindowText(hwnd)
        if window_name:
            all_windows.append({hwnd: window_name})
            print(f"{hwnd:10} -- {window_name}")


def list_of_open_windows() -> list:
    print("List of open windows with their IDs")
    print("window_id \t window_name")
    all_windows: list = []
    win32gui.EnumWindows(winEnumHandler, all_windows)
    return all_windows
