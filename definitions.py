import argparse
import sys, getopt

BUILDFILE= "tix-time-client/Model/build/libs/tix-time-client.jar"
QUESTIONTIMETOOLONG = "More than 1 day to perform test execution.\
Continue? [y/N]"
WRONGANSWER = "Please respond with 'yes' or 'no' " "(or 'y' or 'n').\n"
PROGRAMEXECUTION = 'python3.5 calibration_test'
PROGRAMDESCRIPTION = 'System test launcher'
PROGRAMOPTIONS = '[options]'
LONGUSEROPTION = "--username"
SHORTUSEROPTION = "-u"
HELPUSEROPTION = "Tix 's username"
REQUIREDARGGROUP= 'required arguments'
LONGPASSOPTION = "--password"
SHORTPASSOPTION = "-p"
HELPPASSOPTION = "Tix 's password"
LONGPORTOPTION = "--port"
SHORTPORTOPTION = "-P"
HELPPORTOPTION = "Local port to receive incoming packages"
LONGLOGSDIROPTION = "--logs_dir"
SHORTLOGSDIROPTION = "-l"
HELPLOGSDIROPTION = "Logs files 's destination directory"
LONGINSTALLATIONOPTION = "--installation"
SHORTINSTALLATIONOPTION = "-i"
HELPINSTALLATIONOPTION = "User 's Tix installation name"
LONGTORRENTCONFIGOPTION = "--torrent-file-config"
SHORTTORRENTCONFIGOPTION = "-tfc"
HELPTORRENTCONFIGOPTION = "Torrent configuration files 's path"
GRADLECOMMAND = 'gradle'
GRADLEOPTIONS = ':Model:jar'
TIX_TIME_CLIENT_PATH = "tix-time-client/"
DAYSAMOUNT = 1
SUCCESSRETURN = 0
SLASH = "/"
TEST_DESCRIPTION_YAML = 'description.yml'
START_TIME_INDEX = 'start_time'
MAX_SPEED_INDEX = 'max_speed_kbps'
INTERVAL_INDEX = 'intervals'
CURRENT_PATH ="."
JAVA_COMMAND = 'java'
JAVA_OPTION = '-jar'
CLIENTLOGFILENAME = 'client.log'
SLEEPSECONDSAFTERTORRENTFINISH = 60
NETWORKINTERFACE = 'network_interface'
TIXTIMECLIENTLOGDIR = 'tix-time-client-logs'
'''
PRE: --
POS: Avisa al usuario que falta mas de un dia para la ejecucion de la prueba.
Pregunta si quiere continuar o no. Si el usuario indica que no quiere continuar,
el metodo devuelve False. Si el usuario indica que quiere continuar, devuelve
True. Mientras el usuario no indique una opcion valida, el metodo va a continuar
preguntando.
'''
def continue_execution_if_time_too_long():
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
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
Pre: --
Pos: Devuelve los argumentos de linea de comandos parseados en una estrucura.
Si alguno de los argumentos no esta presente en la linea de comandos, va a
mostrar un mensaje por pantalla indicando el argumento faltante y finaliza.
Si todos los argumentos requeridos estan presenes entonces devuelve una
estructura con los argumentos disponibles para su posterior uso.
'''
def get_and_check_parse_arguments():
    parser = argparse.ArgumentParser(prog=PROGRAMEXECUTION, 
                                     usage='%(prog)s '+ PROGRAMOPTIONS,
                                     description = PROGRAMDESCRIPTION)
    required_named = parser.add_argument_group(REQUIREDARGGROUP)
    required_named.add_argument(LONGUSEROPTION, SHORTUSEROPTION, 
                                help=HELPUSEROPTION,
                                required = True)
    required_named.add_argument(LONGPASSOPTION,SHORTPASSOPTION,
                                help=HELPPASSOPTION,
                                required = True);
    required_named.add_argument(LONGPORTOPTION,SHORTPORTOPTION,
                                help=HELPPORTOPTION,
                                required = True);
    required_named.add_argument(LONGLOGSDIROPTION,SHORTLOGSDIROPTION,
                                help=HELPLOGSDIROPTION,
                                required = True);
    required_named.add_argument(LONGINSTALLATIONOPTION,SHORTINSTALLATIONOPTION,
                                help=HELPINSTALLATIONOPTION,
                                required = True);
    required_named.add_argument(LONGTORRENTCONFIGOPTION,
                                SHORTTORRENTCONFIGOPTION,
                                help=HELPTORRENTCONFIGOPTION,
                                required = True);
    return parser.parse_args()
