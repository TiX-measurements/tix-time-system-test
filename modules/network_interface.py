#!/bin/python3

from subprocess import Popen

class NetworkInterface:

    def __init__(self, interface):
        self.interface = interface

    def downloaded_bytes(self):
        command = ['cat', '/sys/class/net/{}/statistics/rx_bytes'.format(self.interface)]
        process = subprocess.Popen(command, 
                                   stdout=subprocess.PIPE, 
                                   shell=True)

        stdout, stderr = process.communicate()

        return int(stdout)
    