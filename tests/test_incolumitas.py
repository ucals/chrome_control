from random import uniform
from time import sleep
from pathlib import Path
from chrome_control import *


def test_incolumitas():
    print('Trying to start browser')
    start_browser(['bot.incolumitas.com\n'], force_restart_chrome=True)

    # click link to get to the challenge
    print('Trying to click challenge link')
    sleep(3)

    coords = get_coords('li:nth-of-type(3) a')
    print('Clicking on coordinates ' + str(coords))
    human_move(*coords)
    sleep(uniform(0.5, 1.0))

    # press('end')
    # exit(0)

    x = eval_js("document.querySelector('li:nth-of-type(3) a').text").decode()
    print('Clicked on link with text: ' + x)

    # enter username
    username = get_coords('input[name="userName"]')
    human_move(*username, clicks=2)
    sleep(uniform(0.25, 1.25))
    human_typing('IamNotABotISwear\n', speed=(0.005, 0.008))

    sleep(uniform(0.5, 1.0))

    # enter email
    email = get_coords('input[name="eMail"]')
    human_move(*email, clicks=3)
    sleep(uniform(0.25, 1.25))
    human_typing('bot@spambot.com\n', speed=(0.005, 0.008))

    sleep(uniform(0.5, 1.0))

    # agree to the terms
    terms = get_coords('input[name="terms"]')
    human_move(*terms)

    # select cats
    cat = get_coords('#bigCat')
    human_move(*cat)

    # submit
    submit = get_coords('#submit')
    human_move(*submit)

    # press the final enter
    sleep(uniform(2.5, 3.4))
    human_typing('\n', speed=(0.005, 0.008))

    # finally get the page source
    text = get_page_source()
    fname = '/tmp/result.html'
    print(f'Got {len(text) / 2**10} KB of page soure. Saved into {fname}')
    Path(fname).write_text(text.decode())
