import socket
import urllib.request
import requests
from enum import Enum


class Target():
    def __init__(self, hostname_or_ip, port=8907, description=None):
        if self.is_ip_address(hostname_or_ip):
            self.ip = hostname_or_ip
            self.hostname = self.resolve_hostname(self.ip)
        else:
            self.hostname = hostname_or_ip
            self.ip = self.resolve_ip(self.hostname)

        self.port = port

    def is_ip_address(self, text):
        try:
            socket.inet_aton(text)
            return True
        except socket.error:
            return False

    def resolve_ip(self, hostname):
        try:
            return socket.gethostbyname(hostname)
        except socket.gaierror:
            return None

    def resolve_hostname(self, ip):
        try:
            hostname = socket.gethostbyaddr(ip)[0]
        except socket.herror:
            hostname = "(unknown host)"

        return hostname

    def url(self, path=''):
        return "http://{}:{}/{}".format(self.ip, self.port, path)

    def ping(self):
        if self.ip:
            try:
                requests.get(self.url('ping'), timeout=0.2)
                return True
            except:
                return False
        else:
            return False

    def check_status(self):
        if not self.ping():
            return TargetStatus.NO_RESPONSE

        r = requests.get(self.url('info-beamer/status'))
        if r.text == 'running':
            return TargetStatus.INFO_BEAMER_RUNNING
        else:
            return TargetStatus.INFO_BEAMER_STOPPED

    def start(self):
        r = requests.get(self.url('info-beamer/start'))
        print('{}: {}'.format(self.hostname, r.text))

    def stop(self):
        r = requests.get(self.url('info-beamer/stop'))
        print('{}: {}'.format(self.hostname, r.text))

    def restart(self):
        r = requests.get(self.url('info-beamer/restart'))
        print('{}: {}'.format(self.hostname, r.text))

    def start_services(self):
        r = requests.get(self.url('services/start'))
        print('{}: {}'.format(self.hostname, r.text))

    def stop_services(self):
        r = requests.get(self.url('services/stop'))
        print('{}: {}'.format(self.hostname, r.text))

    def restart_services(self):
        r = requests.get(self.url('services/restart'))
        print('{}: {}'.format(self.hostname, r.text))

    def push(self, zip_path):
        files = {'node.zip': open('node.zip', 'rb')}
        r = requests.post(self.url('node/push'), files=files)
        print('{}: {}'.format(self.hostname, r.text))


class TargetStatus(Enum):
    NO_RESPONSE = 0
    INFO_BEAMER_STOPPED = 1
    INFO_BEAMER_RUNNING = 2
