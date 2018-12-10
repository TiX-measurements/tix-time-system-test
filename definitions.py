#!/usr/bin/python3
#
#   File: calibration_test.py
#
#   Modified by: 
#       Eduardo Neira, Luis Ali on November 2018 under the course 'Taller de Programacion 3' in the University of Buenos Aires 
#

import argparse
import sys, getopt

BUILDFILE= "tix-time-client/tix-time-client-cli/build/libs/tix-time-client.jar"
GRADLECOMMAND = 'gradle'
GRADLEOPTIONS = ':tix-time-client-cli:jar'

CURRENT_PATH ="."
JAVA_COMMAND = 'java'
JAVA_OPTION = '-jar'
CLIENTLOGFILENAME = 'client.log'
TIXTIMECLIENTLOGDIR = 'tix-time-client-logs'

QUESTIONTIMETOOLONG = "More than 1 day to perform test execution.\
Continue? [y/N]"
WRONGANSWER = "Please respond with 'yes' or 'no' " "(or 'y' or 'n').\n"
PROGRAMEXECUTION = 'python3 calibration_test'
PROGRAMDESCRIPTION = 'System test launcher'
PROGRAMOPTIONS = '[options]'
LONGUSEROPTION = "--username"
SHORTUSEROPTION = "-u"
HELPUSEROPTION = "Tix's username"
REQUIREDARGGROUP= 'required arguments'
LONGPASSOPTION = "--password"
SHORTPASSOPTION = "-p"
HELPPASSOPTION = "Tix's password"
LONGPORTOPTION = "--port"
SHORTPORTOPTION = "-P"
HELPPORTOPTION = "Local port to receive incoming packages"
LONGLOGSDIROPTION = "--logs_directory"
SHORTLOGSDIROPTION = "-l"
HELPLOGSDIROPTION = "Logs files' destination directory"
LONGINSTALLATIONOPTION = "--installation"
SHORTINSTALLATIONOPTION = "-i"
HELPINSTALLATIONOPTION = "User 's Tix installation name"
LONGTORRENTCONFIGOPTION = "--test-configuration-file"
SHORTTORRENTCONFIGOPTION = "-tcf"
HELPTORRENTCONFIGOPTION = "Test configuration file path"

TIX_TIME_CLIENT_PATH = "tix-time-client/"
TEST_DESCRIPTION_YAML = 'description.yml'
START_TIME_INDEX = 'start_time'
MAX_SPEED_INDEX = 'max_speed_kbps'
INTERVAL_INDEX = 'intervals'
NETWORK_INTERFACE_INDEX = 'network_interface'

DAYSAMOUNT = 1
SUCCESSRETURN = 0
SLEEPSECONDSAFTERTORRENTFINISH = 60

'''
If needs to wait more than one day, the user is asked if he wants to continue with the test.
'''
def continue_execution_if_time_too_long():
    valid = {
        "yes": True, 
        "y":   True, 
        "no":  False, 
        "n":   False
    }

    default="no"

    while True:
        sys.stdout.write(QUESTIONTIMETOOLONG)
        choice = input().lower()
        
        if choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write(WRONGANSWER)

'''
Parse arguments from command. All required arguments must be present. 
These are: username, password, port, installation, logs directory and test configuration file
'''
def parse_arguments():
    parser = argparse.ArgumentParser(prog=PROGRAMEXECUTION, 
                                     usage='%(prog)s '+ PROGRAMOPTIONS,
                                     description = PROGRAMDESCRIPTION)

    required_named = parser.add_argument_group(REQUIREDARGGROUP)
    
    required_named.add_argument(LONGUSEROPTION, SHORTUSEROPTION, 
                                help=HELPUSEROPTION,
                                required = True)
    
    required_named.add_argument(LONGPASSOPTION,SHORTPASSOPTION,
                                help=HELPPASSOPTION,
                                required = True)
    
    required_named.add_argument(LONGPORTOPTION,SHORTPORTOPTION,
                                help=HELPPORTOPTION,
                                required = True)
    
    required_named.add_argument(LONGINSTALLATIONOPTION,SHORTINSTALLATIONOPTION,
                                help=HELPINSTALLATIONOPTION,
                                required = True)
    
    required_named.add_argument(LONGLOGSDIROPTION,SHORTLOGSDIROPTION,
                                help=HELPLOGSDIROPTION,
                                required = True)
    
    required_named.add_argument(LONGTORRENTCONFIGOPTION,
                                SHORTTORRENTCONFIGOPTION,
                                help=HELPTORRENTCONFIGOPTION,
                                required = True)
    
    return parser.parse_args()