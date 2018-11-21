#!/usr/bin/python3
import os;
import subprocess
import argparse
import sys, getopt
import yaml
import datetime
import time
from datetime import timedelta
from subprocess import Popen, PIPE, signal
from modules.torrent_manager import *
import pdb

BUILDFILE= "tix-time-client/Model/build/libs/tix-time-client.jar"
parser = argparse.ArgumentParser()
parser.add_argument("--user", "-u", help="Run all options")
parser.add_argument("--password","-p");
parser.add_argument("--port","-P");
parser.add_argument("--logsPath","-l");
parser.add_argument("--installation","-i");
parser.add_argument("--torrent-file-config","-tfc");

# read arguments from the command line
args = parser.parse_args()

if __name__ == '__main__':
    if ((not args.user) or (not args.password) or (not args.installation) or (not args.port) or (not args.logsPath) or (not args.torrent_file_config)):
        print("Bad arguments. Please type -h or --help");
        sys.exit(-1);
    if (not os.path.exists(BUILDFILE)):
        gradle_build_process=Popen(['gradle', ':Model:jar'], stdout=PIPE, stderr=PIPE, cwd="tix-time-client/")
        gradle_build_process.wait();
    #logfile= open("runlog.txt", "w");
    #pdb.set_trace()
    # Leer el yaml al principio para saber cuando empizan los tests (start time)
    # Hacer un sleep de la resta entre el start time y el tiempo actualself.
    # Despues el start time convertido en epoc. (fijarte dia y hora para construir epoc).
    # Guardar el archivo test_desription.yaml (Va a tener el start time en epoc, el max speed y los intervalos). Guardarlo en la carpeta de los logs (los json))
    # Mandar a ejecutar el cliente y el torrent.
    # Mandar la senal
    with open("config/test.yml", 'r') as stream:
        try:
            default_config = yaml.load(stream);
            now = datetime.datetime.now();
            start = datetime.datetime.strptime(now.strftime('%Y-%m-%d')+":"+default_config['start_time'], '%Y-%m-%d:%H:%M');
            #Cuidado en el siguiente if. Hay precision hasta minutos. Si es el mismo segundo (now y start), la resta entre start y now puede dar negativo.
            if ((now.hour > start.hour) or ((now.hour == start.hour) and (now.minute > start.minute)) or ((now.hour == start.hour) and (now.minute == start.minute) and (now.second > start.second))):
                start = start + timedelta(days=1);
            delay_seconds = (start - now).total_seconds()
            time.sleep(delay_seconds);
            real_start = dict(start_time= datetime.datetime.now().timestamp());
            with open('config/real_start.yml', 'w') as outfile:
                yaml.dump(real_start, outfile, default_flow_style=False)
        except yaml.YAMLError as exc:
            print(exc)
    tix_time_client_process=Popen(['java', '-jar', str(BUILDFILE), str(args.user), str(args.password), str(args.installation), str(args.port), str(args.logsPath)], stdout= PIPE, stderr=PIPE, cwd=".")
    with open(args.torrent_file_config, "r") as test_configuration_file:
        test_configuration = yaml.load(test_configuration_file);
    torrent_manager = TorrentManager(test_configuration['max_speed'], test_configuration['intervals']);
    torrent_manager.run();
    tix_time_client_process.send_signal(signal.SIGINT);
