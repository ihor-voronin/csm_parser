import win32gui


def winEnumHandler(hwnd, ctx):
    if win32gui.IsWindowVisible(hwnd):
        print(f'{hwnd:10} -- {win32gui.GetWindowText(hwnd) or "no-name"}')


def list_of_open_windows():
    print("window_id \t window_name")
    return win32gui.EnumWindows(winEnumHandler, None)
