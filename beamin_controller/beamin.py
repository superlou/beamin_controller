#!/usr/bin/python3
import argparse
import json
import sys
import shutil
import socket
from .target import Target
from .packager import Packager
from .ssdp import discover


def get_targets(only_pingable=True):
    config = json.load(open('config.json'))
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


def package_group(packager, group):
    include = group.get('include', ['*'])
    exclude = group.get('exclude', [])

    if not isinstance(include, list):
        include = [include]

    if not isinstance(exclude, list):
        exclude = [exclude]

    packager.add_matching(include, exclude)


def push_node(group_names):
    config = json.load(open('config.json'))
    push_groups = config['push_groups']

    packager = Packager(config['node_root'], 'node.zip')

    for name in group_names:
        name_found = False

        for group in push_groups:
            if group['name'] == name:
                name_found = True
                package_group(packager, group)

        if not name_found:
            group_names.remove(name)
            print('Push group "{}" not found!'.format(name))

    if len(group_names) > 0:
        print("Pushing data for group(s): {}".format(', '.join(group_names)))

        targets = get_targets()
        for target in targets:
            target.push('node.zip')


class ExtendAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        items = getattr(namespace, self.dest) or []
        items.extend(values)
        setattr(namespace, self.dest, items)


def parse_args(args=None):
    parser = argparse.ArgumentParser(description='Beamin Info-Beamer tools')
    parser.register('action', 'extend', ExtendAction)
    parser.add_argument('-l', '--list', help='list targets', action='store_true')
    parser.add_argument('-p', '--push', help='stop info-beamer',
                        nargs='*', action='extend')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-s', '--start', help='start info-beamer', action='store_true')
    group.add_argument('-x', '--stop', help='stop info-beamer', action='store_true')
    group.add_argument('-d', '--discover', help='discover targets using SSDP', action='store_true')

    args = parser.parse_args(args)

    if isinstance(args.push, list) and (len(args.push) == 0):
        args.push.append('default')

    return args


def main():
    args = parse_args()

    if args.list:
        list_targets()
        sys.exit()

    if args.start:
        start_targets()

    if args.stop:
        stop_targets()

    if args.push:
        push_node(args.push)

    if args.discover:
        discover('beamin_target:control')


if __name__ == '__main__':
    main()
