#!/usr/bin/python3

import os
from time import sleep
from subprocess import Popen, PIPE, DEVNULL

class TorrentClient:

    CWD = os.path.realpath('../torrent_client')
    WAIT_UNTIL_DEAD_TIME = 5

    OPEN_TORRENT_CLIENT_COMMAND = ['java', '-jar', 'Azureus2.jar', '--ui=console']
    LOG_OFF_COMMAND = 'log off\n'
    QUEUE_ALL_COMMAND = 'queue all\n'
    QUIT_COMMAND = 'quit\n'

    #TODO: Delete downloaded torrents and change download directory
    def __init__(self, torrents_path, cwd=self.CWD, log_file=DEVNULL):
        self.process = None
        self.cwd = cwd
        self.log_file = log_file

    def start(self, speed):
        self.process = Popen(self.OPEN_TORRENT_CLIENT_COMMAND,
                             stdin=PIPE,
                             stdout=self.log_file,
                             stderr=self.log_file,
                             cwd=self.cwd,
                             encoding='utf8')

        self.__write_message(self.LOG_OFF_COMMAND)
        self.change_max_download_speed(speed)
        self.__write_message(self.__add_all_torrents_command())
        self.__write_message(self.QUEUE_ALL_COMMAND)

    def change_max_download_speed(self, speed):
        self.__write_message('set max_down '+speed+'\n')

    def stop(self):
        self.__write_message(QUIT_COMMAND)
        sleep(WAIT_UNTIL_DEAD_TIME)    
        self.process.kill()

    def log_file(self):
        return self.LOG_FILE

    def __write_message(self, message):
        self.process.stdin.write(message)
        self.flush()

    def __add_all_torrents_command(self):
        return 'add ' + self.torrents_path + '\n'
