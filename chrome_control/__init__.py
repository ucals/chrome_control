import argparse
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


def main():
    parser = argparse.ArgumentParser(description='Chrome Control CLI')
    subparsers = parser.add_subparsers(
        dest='subcommand_name',
        help='Tools to control Chrome from CLI')

    # create the parser for the "goto" command
    parser_goto = subparsers.add_parser(
        'goto',
        help='Go to a URL')
    parser_goto.add_argument(
        'url',
        type=str,
        help='The URL to go to.')

    # create the parser for the "get-page-source" command
    parser_gps = subparsers.add_parser(
        'get-page-source',
        help='Get the page source')
    parser_gps.add_argument(
        '--destination',
        type=str,
        help='The destination file. Defaults to stdout.')

    # create the parser for the "get-coords" command
    parser_gc = subparsers.add_parser(
        'get-coords',
        help='Get the coordinates of a CSS selector')
    parser_gc.add_argument(
        'selector',
        type=str,
        help='The CSS selector to get the coordinates of.')
    parser_gc.add_argument(
        '--not-randomize-within-bcr',
        action='store_false',
        help='Whether to randomize the coordinates within the bounding client rect.')
    parser_gc.add_argument(
        '--highlight',
        action='store_true',
        help='Whether to highlight the element.')

    # create the parser for the "eval-js" command
    parser_ejs = subparsers.add_parser(
        'eval-js',
        help='Evaluate a JS expression')
    parser_ejs.add_argument(
        'expression',
        type=str,
        help='The JS expression to evaluate.')

    # create the parser for the "start" command
    parser_start = subparsers.add_parser(
        'start',
        help='Start Chrome listening to remote debug')

    # create the parser for the "stop" command
    parser_stop = subparsers.add_parser(
        'stop',
        help='Stop Chrome')

    args = parser.parse_args()

    if args.subcommand_name == 'goto':
        goto(args.url)

    elif args.subcommand_name == 'get-page-source':
        source = get_page_source()
        if args.destination is None:
            print(source)
        else:
            with open(args.destination, 'w') as f:
                f.write(source)

    elif args.subcommand_name == 'get-coords':
        coords = get_coords(
            args.selector,
            randomize_within_bcr=args.not_randomize_within_bcr,
            highlight=args.highlight
        )
        print(coords)

    elif args.subcommand_name == 'eval-js':
        print(eval_js(args.expression))

    elif args.subcommand_name == 'start':
        start_browser()

    elif args.subcommand_name == 'stop':
        close_browser()

    else:
        parser.print_help()
