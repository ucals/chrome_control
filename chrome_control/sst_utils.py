import json
import math
import random
import subprocess
from pathlib import Path


BASE_DIR = Path(__file__).parent.parent


def get_script_path(script_name: str | Path) -> Path:
    return BASE_DIR / 'chrome_control/cdp' / script_name


def goto(url: str, script_name: str = 'goto.js') -> None:
    cmd = f"node {get_script_path(script_name)} '{url}'"
    ps = subprocess.check_output(cmd, shell=True)
    return ps


def get_page_source(script_name: str = 'page_source.js'):
    cmd = f"node {get_script_path(script_name)}"
    ps = subprocess.check_output(cmd, shell=True)
    return ps


def get_coords(
        selector: str,
        randomize_within_bcr: bool = True,
        highlight_bb: bool = False,
        script_name: str = 'coords.js'
) -> tuple | None:
    cmd = f"node {get_script_path(script_name)} '{selector}'"
    coords = subprocess.check_output(cmd, shell=True)
    coords = coords.decode()

    x, y = 0, 0
    try:
        parsed = json.loads(coords)
        x, y = parsed['x'], parsed['y']

        if randomize_within_bcr:
            x += random.randint(0, math.floor(parsed['width'] / 4))
            y += random.randint(0, math.floor(parsed['height'] / 4))

        if highlight_bb:
            # Just add a red thick border around the CSS selector
            # cmd = """var el = document.querySelector('""" + selector + \
            #       """'); if (el) { el.style.border = "2px solid #ff0000"; }"""
            # evalJS(cmd)
            raise NotImplementedError

    except Exception as e:
        print(f'getCoords() failed with Error: {e}')
        return None

    return x, y
