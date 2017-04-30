#!/usr/bin/python3
import json
from random import randint
from asciimatics.screen import Screen
from time import sleep
from .target import Target, TargetStatus

def status_board(screen, targets):
    while True:
        for i, target in enumerate(targets):
            screen.print_at('[ ]', 0, i)
            screen.print_at(target.hostname, 4, i)

            if target.ip:
                screen.print_at(target.ip, 20, i)
            else:
                screen.print_at('unresolved', 20, i, Screen.COLOUR_YELLOW)

            status = target.check_status()
            if status == TargetStatus.NO_RESPONSE:
                screen.print_at('No Response', 40, i, Screen.COLOUR_RED)
            elif status == TargetStatus.INFO_BEAMER_STOPPED:
                screen.print_at('Stopped    ', 40, i, Screen.COLOUR_RED)
            elif status == TargetStatus.INFO_BEAMER_RUNNING:
                screen.print_at('Running    ', 40, i, Screen.COLOUR_GREEN)


        ev = screen.get_key()
        if ev in (ord('Q'), ord('q')):
            return
        screen.refresh()

        sleep(1)


def main():
    config = json.load(open('targets.json'))
    targets = [Target(t['location']) for t in config['targets']]

    Screen.wrapper(status_board, arguments=(targets,))


if __name__ == '__main__':
    main()
