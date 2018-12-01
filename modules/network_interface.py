#!/bin/python3

from subprocess import Popen, PIPE

class NetworkInterface:

    def __init__(self, interface):
        self.interface = interface

    def downloaded_bytes(self):
        command = ['cat /sys/class/net/{}/statistics/rx_bytes'.format(self.interface)]
        process = Popen(command, stdin=None, stdout=PIPE, stderr=None, shell=True)

        stdout, stderr = process.communicate()

        return int(stdout.decode('utf8').strip())
    