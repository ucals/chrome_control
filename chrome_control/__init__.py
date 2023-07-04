import pyautogui

from .behavior import (
    human_move, human_typing, human_scroll, press, tiny_sleep, double_hit
)
from .sst_utils import (
    goto, get_page_source, get_coords, start_browser, eval_js, close_browser
)

# When fail-safe mode is True, moving the mouse to the upper-left
# will raise a pyautogui.FailSafeException that can abort your program:
pyautogui.FAILSAFE = True
