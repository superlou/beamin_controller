import socket
import urllib.request
import shutil
import requests


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
        return socket.gethostbyaddr(ip)[0]

    def url(self, path=''):
        return "http://{}:{}/{}".format(self.ip, self.port, path)

    def ping(self):
        if self.ip:
            try:
                requests.get(self.url('ping'))
                return True
            except:
                return False
        else:
            return False

    def start(self):
        requests.get(self.url('info-beamer/start'))

    def stop(self):
        requests.get(self.url('info-beamer/stop'))

    def restart(self):
        requests.get(self.url('info-beamer/restart'))

    def push_all(self, path):
        shutil.make_archive('node', 'zip', path)
        files = {'node.zip': open('node.zip', 'rb')}
        r = requests.post(self.url('node/push'), files=files)
        print('{}: {}'.format(self.hostname, r.text))
