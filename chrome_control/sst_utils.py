import json
import math
import os
import random
import subprocess
import sys
from pathlib import Path
from time import sleep

import requests

BASE_DIR = Path(__file__).parent.parent
DEFAULT_PATH_ON_MAC = '/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome'


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
            cmd = """var el = document.querySelector('""" + selector + \
                  """'); if (el) { el.style.border = "2px solid #ff0000"; }"""
            eval_js(cmd)

    except Exception as e:
        print(f'getCoords() failed with Error: {e}')
        return None

    return x, y


def eval_js(command: str, script_name: str = 'eval_js.js'):
    with open('/tmp/eval_command.txt', 'w') as f:
        f.write(command)

    cmd = f"node {get_script_path(script_name)}"
    ps = subprocess.check_output(cmd, shell=True)
    return ps


def start_browser(
        args: tuple | list = (),
        start_in_temp_dir: bool = False,
        chrome_profile: str = 'Default',
        chrome_path: str = DEFAULT_PATH_ON_MAC,
        log_path: str | Path = '/tmp',
        sleep_after_start: int = 5,
        force_restart_chrome: bool = False
):
    temp_dir_str = '--user-data-dir=/tmp' if start_in_temp_dir else ''
    out_file = Path(log_path) / 'out.log'
    err_file = Path(log_path) / 'err.log'
    arg_str = ' '.join(args)
    if sys.platform == 'darwin':
        # On MacOS Monterey, we need to start Google Chrome in fullscreen mode
        # to get the correct coordinates.
        cmd = (
            f'{chrome_path} --remote-debugging-port=9222 --start-maximized '
            f'{temp_dir_str} --profile-directory="{chrome_profile}" '
            f'--disable-notifications --start-fullscreen {arg_str} '
            f'1>{out_file} 2>{err_file} &'
        )
    else:
        cmd = (
            f'google-chrome --remote-debugging-port=9222 --start-maximized '
            f'--disable-notifications {arg_str} 1>{out_file} 2>{err_file} &'
        )

    if os.getenv('DOCKER') == '1':
        cmd = (
            f'google-chrome --remote-debugging-port=9222 --no-sandbox '
            f'--disable-notifications --start-maximized --no-first-run '
            f'--disable-gpu '
            f'--no-default-browser-check 1>{out_file} 2>{err_file} &'
        )
        if len(args) > 0:
            print('Warning: args are ignored when running in Docker.')

    subprocess.Popen([cmd], shell=True)
    sleep(random.uniform(sleep_after_start - 1, sleep_after_start + 1))
    if not is_url_reachable('http://127.0.0.1:9222'):
        if force_restart_chrome:
            close_browser()
            start_browser(
                args,
                start_in_temp_dir,
                chrome_profile,
                chrome_path,
                log_path,
                sleep_after_start,
                force_restart_chrome=False
            )
        else:
            raise RuntimeError('Error: Chrome did not start in Dev mode.')


def close_browser(kill_command: str = 'pkill'):
    if sys.platform == 'darwin':
        os.system(f"{kill_command} -9 'Google Chrome'")
    else:
        os.system(f"{kill_command} -9 'google-chrome'")


def is_url_reachable(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return True
        else:
            return False
    except requests.exceptions.RequestException:
        return False
