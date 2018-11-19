#!/usr/bin/python3.6

import yaml
from torrent_client import *

class TorrentManager:

    CLIENT_LOG_FILE = os.path.realpath('../log/torrent_client.log')
    TORRENTS_PATH = os.path.realpath('../torrents')

    def __init__(self, configuration_path):
        with open(configuration_path,'r') as stream:
            self.configuration = yaml.load(stream)
            self.max_speed = self.configuration['max_speed']
            self.intervals = self.configuration['intervals']
            self.start_timer = self.configuration['start_timer']

        self.torrent_client = TorrentClient

    def start(self):
        return None