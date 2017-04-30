#!/usr/bin/python3
import argparse
import json
import sys
from .target import Target


def get_targets(only_pingable=True):
    config = json.load(open('targets.json'))
    targets = [Target(t['location']) for t in config['targets']]

    if only_pingable:
        targets = [target for target in targets if target.ping()]

    return targets


def list_targets():
    targets = get_targets(only_pingable=False)

    for i, target in enumerate(targets):
        status = target.check_status().name
        hostname = target.hostname or ''
        ip = target.ip or ''
        print('{} {:<20} {:<15} {}'.format(i, hostname, ip, status))


def start_targets():
    targets = get_targets()
    for target in targets:
        target.start()


def stop_targets():
    targets = get_targets()
    for target in targets:
        target.stop()


def push_node(path):
    targets = get_targets()
    for target in targets:
        target.push_all(path)


def main():
    parser = argparse.ArgumentParser(description='Beamin Info-Beamer tools')
    parser.add_argument('-l', '--list', help='list targets', action='store_true')
    parser.add_argument('-s', '--start', help='start info-beamer', action='store_true')
    parser.add_argument('-x', '--stop', help='stop info-beamer', action='store_true')
    parser.add_argument('-p', '--push', help='stop info-beamer')
    args = parser.parse_args()

    if args.list:
        list_targets()
        sys.exit()

    if args.start:
        start_targets()

    if args.stop:
        stop_targets()

    if args.push:
        push_node(args.push)


if __name__ == '__main__':
    main()
