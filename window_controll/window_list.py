import win32gui


def winEnumHandler(hwnd, ctx):
    if win32gui.IsWindowVisible(hwnd):
        window_name = win32gui.GetWindowText(hwnd)
        if window_name:
            print(f"{hwnd:10} -- {window_name}")


def list_of_open_windows():
    print("window_id \t window_name")
    return win32gui.EnumWindows(winEnumHandler, None)
