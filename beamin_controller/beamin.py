#!/usr/bin/python3
import argparse
import json
import sys
import shutil
import socket
from .target import Target
from .packager import Packager
from .ssdp import discover


def get_targets(only_pingable=True, select=None):
    config = json.load(open('config.json'))
    targets = [Target(t['location']) for t in config['targets']]

    if only_pingable:
        targets = [target for target in targets if target.ping()]

    if select:
        targets = [target for target in targets
                   if (target.hostname in select) or (target.ip in select)]

    return targets


def list_targets(targets):
    for i, target in enumerate(targets):
        status = target.check_status().name
        hostname = target.hostname or ''
        ip = target.ip or ''
        print('{} {:<20} {:<15} {}'.format(i, hostname, ip, status))


def package_group(packager, group):
    include = group.get('include', ['*'])
    exclude = group.get('exclude', [])

    if not isinstance(include, list):
        include = [include]

    if not isinstance(exclude, list):
        exclude = [exclude]

    packager.add_matching(include, exclude)


def package_node(group_names, zip_filename='node.zip'):
    config = json.load(open('config.json'))
    push_groups = config['push_groups']

    packager = Packager(config['node_root'], zip_filename)

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
        print("Packaged data for group(s): {}".format(', '.join(group_names)))


class ExtendAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        items = getattr(namespace, self.dest) or []
        items.extend(values)
        setattr(namespace, self.dest, items)


def parse_args(args=None):
    parser = argparse.ArgumentParser(description='Beamin Info-Beamer tools')
    parser.register('action', 'extend', ExtendAction)
    parser.add_argument('-l', '--list', help='list all targets',
                        action='store_true')
    parser.add_argument('-p', '--push', help='stop info-beamer',
                        nargs='*', action='extend')
    parser.add_argument('-t', '--target', nargs='+', action='extend',
                        help='apply commands to specified targets')
    parser.add_argument('-d', '--discover', help='discover targets using SSDP',
                        action='store_true')

    group = parser.add_mutually_exclusive_group()
    group.add_argument('-s', '--start', action='store_true',
                       help='start info-beamer and services')
    group.add_argument('-x', '--stop', action='store_true',
                       help='stop info-beamer and services')
    group.add_argument('-r', '--restart', action='store_true',
                       help='restart info-beamer and services')
    group.add_argument('-ss', '--start-services', action='store_true',
                       help='start services only')
    group.add_argument('-xs', '--stop-services', action='store_true',
                       help='stop services only')
    group.add_argument('-rs', '--restart-services', action='store_true',
                       help='restart services only')

    args = parser.parse_args(args)

    if isinstance(args.push, list) and (len(args.push) == 0):
        args.push.append('default')

    return args


def main():
    args = parse_args()

    if args.list:
        list_targets(get_targets(only_pingable=False))
        sys.exit()

    if args.discover:
        discover('beamin_target:control')
        sys.exit()

    if args.push:
        package_node(args.push, 'node.zip')

    if args.target:
        targets = get_targets(select=args.target)
    else:
        targets = get_targets()

    for target in targets:
        if args.start:
            target.start()

        if args.stop:
            target.stop()

        if args.restart:
            target.restart()

        if args.start_services:
            target.start_services()

        if args.stop_services:
            target.stop_services()

        if args.restart_services:
            target.restart_services()

        if args.push:
            target.push('node.zip')


if __name__ == '__main__':
    main()
