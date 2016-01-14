from optparse import OptionParser
from subprocess import check_output, Popen
import time
import sys
from enum import Enum

class Action(Enum):
    KEYBOARD_CONTROL = 0
    RUN_TESTS = 1
    WEB_SERVER = 2
    API_SERVER = 3
    I2C_CHECK = 4

parser = OptionParser()

parser.add_option("-k", "--keyboard-control",
                  action="store_const", const=Action.KEYBOARD_CONTROL, dest="action",
                  help="Start the keyboard control test script.")
parser.add_option("-t", "--run-tests",
                  action="store_const", const=Action.RUN_TESTS, dest="action",
                  help="Run the unit test suite.")
parser.add_option("-w", "--web-server",
                  action="store_const", const=Action.WEB_SERVER, dest="action",
                  help="Start the web interface on a web server.")
parser.add_option("-a", "--api-server",
                  action="store_const", const=Action.API_SERVER, dest="action",
                  help="Start the control API.")
parser.add_option("-i", "--i2c-check",
                  action="store_const", const=Action.I2C_CHECK, dest="action",
                  help="Check attached I2C devices.")


(options, args) = parser.parse_args()

action = options.action

if action == Action.KEYBOARD_CONTROL:
    print "Starting keyboard control script."
    check_output("python tiberius/testing/scripts/keyboard_control.py", shell = True)

elif action == Action.RUN_TESTS:
    print "Starting unit test suite."
    check_output("python tiberius/testing/run_tests.py", shell = True)

elif action == Action.WEB_SERVER:
    print "Starting the web server"
    server = Popen("python tiberius/web-interface/manage.py runserver", shell = True)
    while True:
        try:
            time.sleep(0.1)
        except KeyboardInterrupt:
            Popen.kill(server)
            sys.exit()

elif action == Action.API_SERVER:
    print "Starting the control API."
    server = Popen("python tiberius/control_api/api.py", shell = True)
    while True:
        try:
            time.sleep(0.1)
        except KeyboardInterrupt:
            Popen.kill(server)
            sys.exit()

elif action == Action.I2C_CHECK:
    print "Checking I2C bus for devices"
    result = check_output("i2cdetect -y 1", shell = True)
    print result
