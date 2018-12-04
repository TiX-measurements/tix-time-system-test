#!/bin/python3
#
#   File: calibration_test.py
#
#   Modified by: 
#       Eduardo Neira on November 2018 under the course 'Taller de Programacion 3' in the University of Buenos Aires 
#

from subprocess import Popen, PIPE

class NetworkInterface:

    def __init__(self, interface):
        self.interface = interface

    def downloaded_bytes(self):
        command = ['cat /sys/class/net/{}/statistics/rx_bytes'.format(self.interface)]
        process = Popen(command, stdin=None, stdout=PIPE, stderr=None, shell=True)

        stdout, stderr = process.communicate()

        return int(stdout.decode('utf8').strip())
    