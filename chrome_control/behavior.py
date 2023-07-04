import random
from time import sleep

import pyautogui


def get_dim() -> tuple:
    # current screen resolution width and height
    return pyautogui.size()


def tiny_sleep():
    sleep(random.uniform(0.075, 0.329))


def somewhere_random_close(x: float, y: float, max_dist: float = 120) -> tuple:
    """
    Find a random position close to (x, y)
    with maximal dist @max_dist
    """
    shape = pyautogui.size()
    cnt = 0

    while True:
        rand_x = random.randrange(1, max_dist)
        rand_y = random.randrange(1, max_dist)

        if random.random() > 0.5:
            rand_x *= -1

        if random.random() > 0.5:
            rand_y *= -1

        if x + rand_x in range(0, shape.width):
            if y + rand_y in range(0, shape.height):
                return x + rand_x, y + rand_y

        cnt += 1
        if cnt > 15:
            return x, y


def human_move(x: float, y: float, clicks: int = 1, steps: int = 1):
    """
    Moves like a human to the coordinate (x, y) and
    clicks on the coordinate.

    Randomizes move time and the move type.

    Visits one intermediate coordiante close to the target before
    fine correcting and clicking on the target coordinates.
    """
    width, height = get_dim()

    if steps > 1:  # kek
        far_x, far_y = somewhere_random_close(x, y, min(width, 600))
        pyautogui.moveTo(
            far_x, far_y, random.uniform(0.35, .55), pyautogui.easeOutQuad)
        tiny_sleep()

    if steps > 0:
        closer_x, closer_y = somewhere_random_close(x, y, min(width, 400))
        pyautogui.moveTo(
            closer_x, closer_y, random.uniform(0.25, .40), pyautogui.easeOutQuad)

    # move to an intermediate target close to the destination
    # start fast, end slow
    close_x, close_y = somewhere_random_close(x, y, 50)
    pyautogui.moveTo(
        close_x, close_y, random.uniform(.25, .45), pyautogui.easeOutQuad)

    # click on the main target
    pyautogui.moveTo(x, y, random.uniform(.22, .35))
    tiny_sleep()
    pyautogui.click(clicks=clicks)


def human_scroll(steps: int, clicks: tuple = (5, 20), direction: int = 1):
    for i in range(steps):
        ran_click = random.uniform(*clicks)
        pyautogui.scroll(direction * ran_click)
        sleep(random.uniform(0.5, 1.329))


def double_hit(key1: str, key2: str):
    """
    Sometimes press two keys down at the same time and randomize the
    order of the corresponding key up events to resemble
    human typign closer.
    """
    pyautogui.keyDown(key1)
    tiny_sleep()
    pyautogui.keyDown(key2)
    tiny_sleep()
    if random.random() > 0.5:
        pyautogui.keyUp(key1)
        tiny_sleep()
        pyautogui.keyUp(key2)
    else:
        pyautogui.keyUp(key2)
        tiny_sleep()
        pyautogui.keyUp(key1)


def human_typing(
        text: str,
        speed: tuple = (0.01, 0.025),
        execute_double_hit: bool = False
):
    i = 0
    while i <= len(text):
        if speed:
            sleep(random.uniform(*speed))

        if execute_double_hit is True and random.random() < .3 and i + 1 < len(text):
            double_hit(text[i], text[i + 1])
            i += 2
        else:
            pyautogui.keyDown(text[i])
            pyautogui.keyUp(text[i])
            i += 1

        if i >= len(text):
            break


def click_normal(clicks: int = 1):
    pyautogui.click(clicks=clicks, interval=0.25)


def type_normal(text: str):
    pyautogui.write(text, interval=random.uniform(0.15, 0.25))


def fastwrite(text: str):
    pyautogui.write(text, interval=random.uniform(0.045, 0.075))


def type_write(s: str):
    pyautogui.typewrite(s, interval=0.22)


def press(key: str):
    # pyautogui.press('char', presses=1)
    pyautogui.press(key)


def move_randomly(steps: int = 2):
    width, height = get_dim()
    width = min(1920, width)
    # move the mouse a bit
    for i in range(steps):
        human_move(*(
            random.randrange(0, width - 50), random.randrange(0, height - 50)),
                  clicks=0, steps=2)
        sleep(random.uniform(0.25, 1.0))
