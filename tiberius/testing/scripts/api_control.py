import sys
from tiberius.logger import logger
import logging
d_logger = logging.getLogger('tiberius.testing.api_control')
import tty
import termios
import time
import urllib2
import argparse


def getKey():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i', "--ip-address", help="The IP address that the control API is running on.", required=True)
    args = parser.parse_args()

    ip_address = args.ip_address

    motors_url = "http://" + ip_address + ":8000/motors"
    while(True):

        key = getKey()
        d_logger.debug("Key %s pressed", key)
        if(key == 'c' or key == 'C'):
            urllib2.urlopen(motors_url + "?stop=true").read()
            sys.exit(0)
        elif(key == 'w'):
            urllib2.urlopen(motors_url + "?forward=50").read()
        elif(key == 'W'):
            urllib2.urlopen(motors_url + "?forward=100").read()
        elif(key == 'a'):
            urllib2.urlopen(motors_url + "?left=40").read()
        elif(key == 'A'):
            urllib2.urlopen(motors_url + "?left=100").read()
        elif(key == 's'):
            urllib2.urlopen(motors_url + "?backward=50").read()
        elif(key == 'S'):
            urllib2.urlopen(motors_url + "?backward=100").read()
        elif(key == 'd'):
            urllib2.urlopen(motors_url + "?right=40").read()
        elif(key == 'D'):
            urllib2.urlopen(motors_url + "?right=100").read()
        elif(key == ' '):
            urllib2.urlopen(motors_url + "?stop=true").read()
            time.sleep(0.1)

        # c.motors.stop()
