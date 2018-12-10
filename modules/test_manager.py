#!/usr/bin/python3
#
#   File: calibration_test.py
#
#   Modified by: 
#       Eduardo Neira on November 2018 under the course 'Taller de Programacion 3' in the University of Buenos Aires 
#

import os
import datetime
from time import sleep, time
from modules.torrent_client import TorrentClient
from modules.network_interface import NetworkInterface

class TestManager:

    TORRENTS_PATH              = os.path.realpath('torrents')
    CLIENT_LOG_FILENAME        = 'torrent_client.log'
    NETWORK_USAGE_LOG_FILENAME = 'network_usage.log'

    MINUTE_IN_SECONDS = 60

    def __init__(self, max_speed, intervals, network_interface, logs_path):
        self.max_speed = max_speed
        self.intervals = intervals
        self.logs_path = logs_path 
        
        self.torrent_client = TorrentClient(self.TORRENTS_PATH,
                                            log_file=open(self.__client_log_path(), 'w'))

        self.network_interface = NetworkInterface(network_interface)

    def run(self):
        self.downloaded_bytes = self.network_interface.downloaded_bytes()

        print('{}  =>  Torrent started'.format(datetime.datetime.now()))
        self.torrent_client.start()
        
        with open(self.__network_usage_log_path(), 'w') as network_usage_log:
            network_usage_log.write('time_epoch|speed_kbps\n')

            for interval in self.intervals:
                speed = self.__percentage_to_speed(interval['speed_percentage'])
                print('{}  =>  Changed speed to {}'.format(datetime.datetime.now(), speed))
                self.torrent_client.change_max_download_speed(speed)
                
                for i in range(0, interval['duration_minutes']):
                    sleep(self.MINUTE_IN_SECONDS)

                    self.__log_estimated_speed(network_usage_log, self.MINUTE_IN_SECONDS)

                    self.torrent_client.clean_torrent_downloads()
                    
                    self.torrent_client.show_torrents()

        print('{}  =>  Stopping Torrent'.format(datetime.datetime.now()))
        self.torrent_client.stop()
        print('{}  =>  Torrent Stopped'.format(datetime.datetime.now()))

    def __log_estimated_speed(self, log_file, delta_time):
        updated_downloaded_bytes = self.network_interface.downloaded_bytes()
        
        if updated_downloaded_bytes < self.downloaded_bytes:
            print('RX bytes counter reset. Old: {}, New: {}'.format(self.downloaded_bytes, updated_downloaded_bytes))
            self.downloaded_bytes -= NetworkInterface.MAX_DOWNLOADED_BYTES  
        
        estimated_speed_kbps = (updated_downloaded_bytes - self.downloaded_bytes) * 8 / (1000 * delta_time)  
        
        log_file.write('{}|{}\n'.format(time(), estimated_speed_kbps))
        
        self.downloaded_bytes = updated_downloaded_bytes

    def __percentage_to_speed(self, speed_percentage):
        return int(self.max_speed * speed_percentage / 100.0)

    def __client_log_path(self):
        return '{}/{}'.format(self.logs_path, self.CLIENT_LOG_FILENAME)

    def __network_usage_log_path(self):
        return '{}/{}'.format(self.logs_path, self.NETWORK_USAGE_LOG_FILENAME) 