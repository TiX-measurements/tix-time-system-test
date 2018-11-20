#!/usr/bin/python3
import os;
import subprocess
import argparse
import sys, getopt
import yaml
from subprocess import Popen, PIPE, signal
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
        print("no existe. Hay que hacer build");
        gradle_build_process=Popen(['gradle', ':Model:jar'], stdout=PIPE, stderr=PIPE, cwd="tix-time-client/")
        gradle_build_process.wait();
    else:
        print("ya existe el build");
    logfile= open("runlog.txt", "w");
    #pdb.set_trace()
    # Leer el yaml al principio para saber cuando empizan los tests (start time)
    # Hacer un sleep de la resta entre el start time y el tiempo actualself.
    # Despues el start time convertido en epoc. (fijarte dia y hora para construir epoc).
    # Guardar el archivo test_desription.yaml (Va a tener el start time en epoc, el max speed y los intervalos). Guardarlo en la carpeta de los logs (los json))
    # Mandar a ejecutar el cliente y el torrent.
    # Mandar la senal
    tix_time_client_process=Popen(['java', '-jar', str(BUILDFILE), str(args.user), str(args.password), str(args.installation), str(args.port), str(args.logsPath)], stdout= logfile, stderr=PIPE, cwd=".")
    with open(args.torrent_file_config, "r") as test_configuration_file:
        test_configuration = yaml.load(test_configuration_file);
    torrent_manager = TorrentManager(test_configuration['max_speed'], test_configuration['intervals']);
    torrent_manager.run();
    tix_time_client_process.send_signal(signal.SIGINT);
