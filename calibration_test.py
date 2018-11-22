#!/usr/bin/python3
import os;
import subprocess
import yaml
import datetime
import time
from definitions import *
from pathlib import Path
from datetime import timedelta
from subprocess import Popen, PIPE, DEVNULL, signal
from modules.torrent_manager import *
import pdb


'''
Pre: --
Pos: Ejecuta gradle :Model:jar. El proyecto tix-time-client debe estar al mismo
nivel en el file system que este mismo archivo (calibration_test.py).
Este metodo espera a que termina el build y finaliza.
'''
def build_tix_time_client():
    gradle_build_process=Popen([GRADLECOMMAND, GRADLEOPTIONS],\
                               stdout=PIPE,\
                               stderr=PIPE,\
                               cwd=TIX_TIME_CLIENT_PATH)
    gradle_build_process.wait();
'''
PRE: Recibe el tiempo de inicio de la prueba, leido desde el archivo de
configuracion pasado por parametro (torrent-file-config)
POS: Devuelve el delay en segundos desde el tiempo actual de ejecucion hasta el
tiempo de inicio de la prueba.
Si el tiempo actual de ejecucion es mayor al tiempo indicado en el archivo de
configuracion (torrent-file-config), entonces a la diferncia de tiempo le
agrega un dia. Es decir, si desde el archivo de configuracion se lee start_time
igual a 15:30 y se ejecuta calibration_test a las 15:35, se agrega un retardo de
ejecucion de un 1 dia. Hay que esperar hasta las 15:30 del dia siguiente.
'''
def get_time_delay(start_value):
    now = datetime.datetime.now();
    start_time_string_representation =now.strftime('%Y-%m-%d')+":"+ start_value
    start= datetime.datetime.strptime(start_time_string_representation,\
                                      '%Y-%m-%d:%H:%M');
    if (now > start):
        if (continue_execution_if_time_too_long()):
            start = start + timedelta(days=DAYSAMOUNT);
        else:
            sys.exit(SUCCESSRETURN);
    return (start - now).total_seconds()
'''
PRE: Recibe el path donde se guardan los archivos logs
POS: Toma el tiempo al instante de la ejecucion, crea el archivo real_start.yml
en el path donde se guardan los archivos logs (si no existe el path, lo crea),
y sobre este archivo escribe el valor del tiempo al momento de la ejecucion en
formato epoch.
'''
def save_real_start_time_epoch_in_yml_file(logs_path):
    real_start = dict(start_time= datetime.datetime.now().timestamp());
    logsDirectory = str(Path.home()) +SLASH+logs_path;
    real_start_yml_file = logsDirectory +SLASH+REALSTARTYMLFILE;
    if not os.path.exists(logsDirectory):
        os.makedirs(logsDirectory)
    with open(real_start_yml_file, 'w') as outfile:
        yaml.dump(real_start, outfile, default_flow_style=False)
'''
PRE: Recibe el stream correspondiente a la apertura del archivo de configuracion
torrent_file_config para poder obtener los valores de configuracion del torrent,
y el path donde se guardan los archivos logs para poder crear el archivo yml
con el tiempo de inicio real de la medicion (real_start).
POS: Obtiene el tiempo de inicio desde el archivo torrent_file_config. Calcula
la diferencia entre este tiempo obtenido y el tiempo actual
(al momento de ejecucion). Espera hasta llegar al tiempo de inicio. Transcurrido
ese tiempo, guarda el tiempo de ejecucion en ese preciso momento en el
archivo start_time.yml en la carpeta donde se guardan los logs
'''
def wait_until_start_time_and_save_real_start_time_epoch_in_file(config_stream,\
                                                                 logs_path):
    config = yaml.load(config_stream);
    delay_seconds = get_time_delay(config[START_TIME_INDEX]);
    time.sleep(delay_seconds);
    save_real_start_time_epoch_in_yml_file(logs_path);
'''
PRE: Recibe el path del archivo de configuracion del torrent
(torrent_file_config)
POS: Lee desde el archivo de configuracion el valor de la velocidad maxima
de decarga y los intervalos que indican la duracion en minutos y el porcentaje
de velocidad a utilizar en dicho intervalo. Con estos valores se crea el
TorrentManager y se lo ejecuta. El metodo finaliza tras la finalizacion de la
ejecucion del TorrentManager.
'''
def launch_torrent_manager(torrent_file_config):
    with open(torrent_file_config, "r") as test_configuration_file:
        test_configuration = yaml.load(test_configuration_file);
        max_speed = test_configuration[MAX_SPEED_INDEX];
        intervals = test_configuration[INTERVAL_INDEX];
        torrent_manager = TorrentManager(max_speed,intervals);
        torrent_manager.run();
'''
PRE: Recibe los argumentos pasados por parametros
POS: Toma los argumentos necesarios para ejecutar el cliente. Ejecuta el cliente
en un subproceso. Luego lanza el TorrentManager. Tras la finalizacion del
TorrentManager, envia SIGINT al suproceso cliente para terminarlo gracefully.
'''
def launch_tix_client_and_torrent_manager(args):
    tix_client_execution_args = [JAVA_COMMAND, JAVA_OPTION, \
                                 str(BUILDFILE),\
                                 str(args.username),\
                                 str(args.password),\
                                 str(args.installation),\
                                 str(args.port),\
                                 str(args.logs_path)]


    tix_time_client_process=Popen(tix_client_execution_args,\
                                 stdout= open(CLIENTLOGFILEPATH,'w'),\
                                 stderr=DEVNULL,\
                                 cwd=CURRENT_PATH)
    launch_torrent_manager(args.torrent_file_config)
    time.sleep(SLEEPSECONDSAFTERTORRENTFINISH)
    tix_time_client_process.send_signal(signal.SIGINT);
'''
PRE: --
POS: Leer el yaml al principio para saber cuando empizan los tests (start time).
 Hacer un sleep de la resta entre el start time y el tiempo actual.
 Despues calcula el start time convertido en epoch.
 Guardar el archivo test_desription.yaml (Va a tener el start time en epoch,
 el max speed y los intervalos). Guardarlo en la carpeta de los logs (los json))
 Mandar a ejecutar el cliente y el torrent.
 Mandar la senal SIGINT
'''
if __name__ == '__main__':
    args= get_and_check_parse_arguments();
    if (not os.path.exists(BUILDFILE)):
        build_tix_time_client()
    with open(args.torrent_file_config, 'r') as config_stream:
        try:
            wait_until_start_time_and_save_real_start_time_epoch_in_file(\
                                                                config_stream,\
                                                                args.logs_path)
            launch_tix_client_and_torrent_manager(args)
        except yaml.YAMLError as exc:
            print(exc)
