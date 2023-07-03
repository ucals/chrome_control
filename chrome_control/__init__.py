import os
import pyautogui
from .sst_utils import goto, get_page_source, get_coords


if os.getenv('DOCKER') == '1':
    from pyvirtualdisplay.display import Display

    disp = Display(visible=True, size=(1920, 1080), backend="xvfb",
                   use_xauth=True)
    disp.start()

    print('Started display!')
    print(f'DISPLAY = {os.environ["DISPLAY"]}')

    import Xlib.display
    pyautogui._pyautogui_x11._display = Xlib.display.Display(
        os.environ['DISPLAY'])
    print('Hello, world from docker!')
else:
    print('Hello, world from local!')

# When fail-safe mode is True, moving the mouse to the upper-left
# will raise a pyautogui.FailSafeException that can abort your program:
pyautogui.FAILSAFE = True


