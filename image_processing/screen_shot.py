import time
from typing import Optional

import win32con
import win32ui
from PIL import Image
import win32gui

from config import Config


def screen_shoot(window_id: int) -> Optional[Image.Image]:
    # get dimensions of window
    left, top, right, bot = win32gui.GetWindowRect(window_id)
    w = right - left
    h = bot - top

    win32gui.SetForegroundWindow(window_id)
    # time.sleep(1.0)

    hdesktop = win32gui.GetDesktopWindow()
    hwndDC = win32gui.GetWindowDC(hdesktop)
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()

    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)

    saveDC.SelectObject(saveBitMap)

    result = saveDC.BitBlt((0, 0), (w, h), mfcDC, (left, top), win32con.SRCCOPY)

    bmpinfo = saveBitMap.GetInfo()
    bmpstr = saveBitMap.GetBitmapBits(True)

    im = Image.frombuffer(
        "RGB", (bmpinfo["bmWidth"], bmpinfo["bmHeight"]), bmpstr, "raw", "BGRX", 0, 1
    )

    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hdesktop, hwndDC)

    if result is not None:
        return None

    # im.show()
    # im.save("test.png")
    return im
