#!/usr/bin/python3

import os
import glob
from time import sleep
from subprocess import Popen, PIPE, DEVNULL

class TorrentClient:

    WAIT_UNTIL_DEAD_TIME       = 5
    WAIT_TIME_BETWEEN_COMMANDS = 1

    CWD = os.path.realpath('torrent_client')
    DOWNLOAD_PATH = os.path.realpath('torrent_downloads')

    OPEN_TORRENT_CLIENT_COMMAND = ['java', '-jar', 'Azureus2.jar', '--ui=console']
    LOG_OFF_COMMAND             = 'log off\n'
    REMOVE_ALL_TORRENTS_COMMAND = 'remove all\n'
    QUIT_COMMAND                = 'quit\n'
    SHOW_TORRENTS_COMMAND       = 'show torrents\n'
    FORCE_START_ALL_COMMAND     = 'forcestart all\n'
    STOP_ALL_TORRENTS_COMMAND   = 'stop all\n'
    SET_DEFAULT_SAVE_PATH       = 'set "Default save path" "' + DOWNLOAD_PATH + '" string\n'
    SET_MAX_UPLOAD_0            = 'set max_up 0'

    def __init__(self, torrents_path, cwd=CWD, log_file=DEVNULL):
        self.process = None
        self.torrents_path = torrents_path
        self.cwd = cwd
        self.log_file = log_file
        self.idle = True
        os.makedirs(self.DOWNLOAD_PATH, exist_ok=True)

    def start(self):
        self.idle = False
        self.process = Popen(self.OPEN_TORRENT_CLIENT_COMMAND,
                             stdin=PIPE,
                             stdout=self.log_file,
                             stderr=DEVNULL,
                             cwd=self.cwd)

        sleep(self.WAIT_TIME_BETWEEN_COMMANDS)
        self.__write_message(self.SET_MAX_UPLOAD_0)
        self.__write_message(self.LOG_OFF_COMMAND)
        self.__write_message(self.SET_DEFAULT_SAVE_PATH)
        sleep(self.WAIT_TIME_BETWEEN_COMMANDS)
        self.show_torrents()
        sleep(self.WAIT_TIME_BETWEEN_COMMANDS)
        self.__write_message(self.REMOVE_ALL_TORRENTS_COMMAND)
        sleep(self.WAIT_TIME_BETWEEN_COMMANDS)
        self.__delete_torrents_downloaded()
        self.__write_message(self.__add_all_torrents_command())
        sleep(self.WAIT_TIME_BETWEEN_COMMANDS)
        self.show_torrents()
        sleep(self.WAIT_TIME_BETWEEN_COMMANDS)
        self.__write_message(self.FORCE_START_ALL_COMMAND)        
        
    def change_max_download_speed(self, speed):
        self.__write_message('set max_down {}\n'.format(self.__speed_to_kBps(speed)))
            
        if speed == 0 and not self.idle:
            self.idle = True
            self.show_torrents()
            self.__write_message(self.STOP_ALL_TORRENTS_COMMAND)
        elif speed > 0 and self.idle:
            self.idle = False
            self.show_torrents()
            self.__write_message(self.FORCE_START_ALL_COMMAND)

    def show_torrents(self):
        self.__write_message(self.SHOW_TORRENTS_COMMAND)

    def stop(self):
        self.__write_message(self.QUIT_COMMAND)
        self.process.wait()    

    def log_file(self):
        return self.LOG_FILE

    def __write_message(self, message):
        self.process.stdin.write(message.encode('utf-8'))
        self.process.stdin.flush()

    def __add_all_torrents_command(self):
        return 'add '+self.torrents_path+'\n'

    def __delete_torrents_downloaded(self):
        files = glob.glob(self.DOWNLOAD_PATH+'/*')
        
        for file in files:
            os.remove(file)

    def __speed_to_kBps(self, speed_kbps):
        return speed_kbps // 8