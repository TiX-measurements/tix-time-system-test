#!/usr/bin/python3
#
#   File: calibration_test.py
#
#   Modified by: 
#       Eduardo Neira, Luis Ali on November 2018 under the course 'Taller de Programacion 3' in the University of Buenos Aires 
#

import os
import time
import yaml
import datetime
from definitions import *
from datetime import timedelta
from subprocess import Popen, PIPE, DEVNULL, signal
from modules.test_manager import TestManager

'''
Builds grandle jar from the tix-time-client downloaded. 
The main process waits for the build subprocess to finish.
'''
def build_tix_time_client():
    gradle_build_process = Popen([GRADLECOMMAND, GRADLEOPTIONS],
                                 stdout=PIPE,
                                 stderr=PIPE,
                                 cwd=TIX_TIME_CLIENT_PATH)

    gradle_build_process.wait()

'''
Calculates the time delay to wait in seconds from the start value specified in HH:MM
The time delay can't exceed 24 hours
'''
def get_time_delay(start_value):
    now = datetime.datetime.now()

    start_time_string_representation = '{}:{}'.format(now.strftime('%Y-%m-%d'), start_value)
    
    start= datetime.datetime.strptime(start_time_string_representation,
                                      '%Y-%m-%d:%H:%M')
    
    if (now > start):
        if (continue_execution_if_time_too_long()):
            start = start + timedelta(days=DAYSAMOUNT)
        else:
            sys.exit(SUCCESSRETURN)

    return (start - now).total_seconds()

'''
Dumps test description yaml in logs directory.
Start time inside description is changed to the epoch time of the actual start of the test.
'''
def save_test_description(description_config, logs_directory):
    description_config[START_TIME_INDEX] = datetime.datetime.now().timestamp()

    real_start_yml_file = '{}/{}'.format(logs_directory, TEST_DESCRIPTION_YAML)

    with open(real_start_yml_file, 'w') as outfile:
        yaml.dump(description_config, outfile, default_flow_style=False)

'''
Waits until the start time is reached. Also dumps the test configuration in the logs directory
'''
def wait_until_start_time(start_time):
    delay_seconds = get_time_delay(start_time)
    
    print('Test will start in {} minutes'.format(delay_seconds/60.0))
    
    time.sleep(delay_seconds)

'''
Returns logs directory absolute path. If the directory does not exists, it is created
'''
def logs_directory_path(logs_directory):
    logs_directory_absolute_path = '{}/{}'.format(os.path.expanduser('~'), logs_directory)
    
    os.makedirs(logs_directory_absolute_path, exist_ok=True)

    return logs_directory_absolute_path


'''
Creates TestManager from test configuration and logs directory path and run the calibration test
'''
def run_test(test_configuration, logs_directory):
    print('Starting calibration test')

    max_speed = test_configuration[MAX_SPEED_INDEX]
    intervals = test_configuration[INTERVAL_INDEX]
    network_interface = test_configuration[NETWORK_INTERFACE_INDEX]

    test_manager = TestManager(max_speed, intervals, network_interface, logs_directory)
    test_manager.run()

'''
Starts a subprocess for the tix time client with the username, password, installation, port 
and client_logs_directory specified. The STDOUT of the subprocess is stored in the test_logs_directory
'''
def start_tix_time_client(username, password, installation, port, client_logs_directory, test_logs_directory):
    print('Starting tix time client')

    tix_client_execution_args = [JAVA_COMMAND, JAVA_OPTION, 
                                 str(BUILDFILE),
                                 str(username),
                                 str(password),
                                 str(installation),
                                 str(port),
                                 '{}/{}'.format(client_logs_directory, TIXTIMECLIENTLOGDIR)]

    tix_time_client_process = Popen(tix_client_execution_args,
                                    stdout=open('{}/{}'.format(test_logs_directory, CLIENTLOGFILENAME), 'w'),
                                    stderr=DEVNULL,
                                    cwd=CURRENT_PATH)

    return tix_time_client_process
    
'''
Waits 1 minute after torrents finishes to get the last log file. After that, a SIGINT signal is sent
to the tix time client process to stop it
'''
def stop_tix_time_client(tix_time_client_process):
    print('Stopping tix time client')

    time.sleep(SLEEPSECONDSAFTERTORRENTFINISH)

    tix_time_client_process.send_signal(signal.SIGINT)

    print('Tix time client stopped')

'''
Calibration test flow:
    Parses all the arguments required.
    Builds the client if it was not builded before.
    Saves the test description yaml with the start time modified
    Start the tix time client
    Run test manager with the test configuration file
    Stops tix time client
'''
if __name__ == '__main__':
    args = parse_arguments()

    test_logs_directory = logs_directory_path(args.logs_directory)
    
    if (not os.path.exists(BUILDFILE)):
        build_tix_time_client()

    with open(args.test_configuration_file, 'r') as test_configuration_file:
        try:
            test_configuration = yaml.load(test_configuration_file)

            wait_until_start_time(test_configuration[START_TIME_INDEX])

            save_test_description(test_configuration, test_logs_directory)
            
            tix_time_client_process = start_tix_time_client(args.username,
                                                            args.password,
                                                            args.installation,
                                                            args.port,
                                                            args.logs_directory,
                                                            test_logs_directory)

            run_test(test_configuration, test_logs_directory)

            stop_tix_time_client(tix_time_client_process)

        except yaml.YAMLError as exception:
            print(exception)