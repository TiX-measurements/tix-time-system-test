#!/usr/bin/python3

import os
import datetime
from time import sleep
from modules.torrent_client import *

class TestManager:

    LOG_PATH        = 'log'
    CLIENT_LOG_FILE = os.path.realpath(LOG_PATH+'/torrent_client.log')
    TORRENTS_PATH   = os.path.realpath('torrents')

    MINUTE_IN_SECONDS = 60

    def __init__(self, max_speed, intervals):
        self.max_speed = max_speed
        self.intervals = intervals
        os.makedirs(self.LOG_PATH, exist_ok=False)
        self.torrent_client = TorrentClient(self.TORRENTS_PATH,
                                            log_file=open(self.CLIENT_LOG_FILE,'w'))

    def run(self):
        print('{}  =>  Torrent started'.format(datetime.datetime.now()))
        self.torrent_client.start()

        for interval in self.intervals:
            speed = self.__percentage_to_speed(interval['speed_percentage'])
            print('{}  =>  Changed speed to {}'.format(datetime.datetime.now(),speed))
            self.torrent_client.change_max_download_speed(speed)
            
            for i in range(0, interval['duration_minutes']):
                sleep(self.MINUTE_IN_SECONDS)
                self.torrent_client.show_torrents()

        print('{}  =>  Torrent Stopped'.format(datetime.datetime.now()))
        self.torrent_client.stop()

    def __percentage_to_speed(self, speed_percentage):
        return int(self.max_speed * speed_percentage / 100.0)
