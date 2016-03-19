import sys
from tiberius.control.control import Control
from tiberius.logger import logger
import logging
d_logger = logging.getLogger('tiberius.testing.keyboard_control')
import tty
import termios
import time

c = Control()


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
    while(True):

        key = getKey()
        d_logger.debug("Key %s pressed", key)
        if(key == 'c'):
            c.motors.stop()
            sys.exit(0)
        elif(key == 'C'):
            c.motors.stop()
            sys.exit(0)
        elif(key == 'w'):
            c.motors.setSpeedPercent(50)
            c.motors.moveForward()
        elif(key == 'W'):
            c.motors.setSpeedPercent(100)
            c.motors.moveForward()
        elif(key == 'a'):
            c.motors.setSpeedPercent(40)
            c.motors.turnLeft()
        elif(key == 'A'):
            c.motors.setSpeedPercent(100)
            c.motors.turnLeft()
        elif(key == 's'):
            c.motors.setSpeedPercent(50)
            c.motors.moveBackward()
        elif(key == 'S'):
            c.motors.setSpeedPercent(100)
            c.motors.moveBackward()
        elif(key == 'd'):
            c.motors.setSpeedPercent(50)
            c.motors.turnRight()
        elif(key == 'D'):
            c.motors.setSpeedPercent(100)
            c.motors.turnRight()
        elif(key == ' '):
            c.motors.stop()
            time.sleep(0.1)
        # c.motors.stop()
