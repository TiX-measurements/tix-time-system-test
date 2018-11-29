#!/bin/python3

from subprocess import Popen

class NetworkInterface:

    def __init__(self, interface):
        self.interface = interface
        self.bytes_downloaded = 0


    def __check_downloaded_bytes(self):
        command = 'cat /sys/class/net/{}/statistics/rx_bytes'.format(self.interface)


    