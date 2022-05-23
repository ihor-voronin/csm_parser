from window_control.screen_shot import make_screen_shoot
from window_control.window_control import (
    click,
    maximize_window,
    minimize_window,
    page_down,
    scroll,
    set_window_position,
)
from window_control.window_list import get_window_id_from_opened_windows

__all__ = [
    "make_screen_shoot",
    "set_window_position",
    "click",
    "scroll",
    "page_down",
    "minimize_window",
    "maximize_window",
    "get_window_id_from_opened_windows",
]
