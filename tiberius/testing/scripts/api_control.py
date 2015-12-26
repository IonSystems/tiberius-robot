import sys
from tiberius.logger import logger
import logging
d_logger = logging.getLogger('tiberius.testing.api_control')
import tty, termios, time
import urllib2



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

    motors_url = "http://10.113.211.251:8000/motors"
    while(True):

        key = getKey()
        d_logger.debug("Key %s pressed", key)
        if(key == 'c'):
            c.motors.stop()
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

        #c.motors.stop()
