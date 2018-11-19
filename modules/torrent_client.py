#!/usr/bin/python3.6

import os
from time import sleep
from subprocess import Popen, PIPE, DEVNULL

class TorrentClient:

    WAIT_UNTIL_DEAD_TIME = 5
    WAIT_TIME_BETWEEN_COMMANDS = 1

    CWD = os.path.realpath('torrent_client')

    OPEN_TORRENT_CLIENT_COMMAND = ['java', '-jar', 'Azureus2.jar', '--ui=console']
    LOG_OFF_COMMAND = 'log off\n'
    REMOVE_ALL_TORRENTS_COMMAND = 'remove all\n'
    QUEUE_ALL_TORRENTS_COMMAND = 'queue all\n'
    QUIT_COMMAND = 'quit\n'
    SHOW_TORRENTS_COMMAND = 'show torrents\n'

    #TODO: Delete downloaded torrents and change download directory
    def __init__(self, torrents_path, cwd=CWD, log_file=DEVNULL):
        self.process = None
        self.torrents_path = torrents_path
        self.cwd = cwd
        self.log_file = log_file

    def start(self):
        self.process = Popen(self.OPEN_TORRENT_CLIENT_COMMAND,
                             stdin=PIPE,
                             stdout=self.log_file,
                             stderr=DEVNULL,
                             cwd=self.cwd,
                             encoding='utf8')

        self.show_torrents()
        sleep(self.WAIT_TIME_BETWEEN_COMMANDS)
        self.__write_message(self.LOG_OFF_COMMAND)
        sleep(self.WAIT_TIME_BETWEEN_COMMANDS)
        self.__write_message(self.REMOVE_ALL_TORRENTS_COMMAND)
        sleep(self.WAIT_TIME_BETWEEN_COMMANDS)
        self.__write_message(self.__add_all_torrents_command())
        sleep(self.WAIT_TIME_BETWEEN_COMMANDS)
        self.show_torrents()
        sleep(self.WAIT_TIME_BETWEEN_COMMANDS)
        self.__write_message(self.QUEUE_ALL_TORRENTS_COMMAND)

    def change_max_download_speed(self, speed):
        self.__write_message('set max_down '+str(speed)+'\n')
        self.show_torrents()

    def show_torrents(self):
        self.__write_message(self.SHOW_TORRENTS_COMMAND)

    def stop(self):
        self.__write_message(self.QUIT_COMMAND)
        sleep(self.WAIT_UNTIL_DEAD_TIME)    
        self.process.kill()

    def log_file(self):
        return self.LOG_FILE

    def __write_message(self, message):
        self.process.stdin.write(message)
        self.process.stdin.flush()

    def __add_all_torrents_command(self):
        return 'add '+self.torrents_path+'\n'