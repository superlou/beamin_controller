#!/usr/bin/python3
import argparse
import json
import sys
from .target import Target


def list_targets():
    config = json.load(open('targets.json'))
    targets = [Target(t['location']) for t in config['targets']]

    for i, target in enumerate(targets):
        print('{} {:<20} {}'.format(i, target.hostname, target.ip))


def start_targets():
    config = json.load(open('targets.json'))
    targets = [Target(t['location']) for t in config['targets']]
    targets = [target for target in targets if target.ping()]

    for target in targets:
        target.start()


def push_node(path):
    config = json.load(open('targets.json'))
    targets = [Target(t['location']) for t in config['targets']]
    targets = [target for target in targets if target.ping()]

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

    if args.push:
        push_node(args.push)


if __name__ == '__main__':
    main()
