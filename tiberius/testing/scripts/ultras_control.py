#!/usr/bin/env python
import sys
from tiberius.control.control import Control
from tiberius.control.actuators import MotorState
from tiberius.logger import logger
import tty
import termios
import time
import logging
d_logger = logging.getLogger('tiberius.testing.keyboard_control')


c = Control()
ultras = c.ultrasonics


def getKey():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def collision_detection();
        # Use ultrasonics to prevent collisions.
        if ultras.frontHit() and c.motors.state == MotorState.FORWARD:
            c.motors.stop()

        if ultras.rearHit() and c.motors.state == MotorState.BACKWARD:
            c.motors.stop()

        # If we are turning, any edge could be hit, so check all sensors
        if (ultras.anythingHit() and
            (c.motors.state == MotorState.RIGHT or
            c.motors.state == MotorState.LEFT)):
            c.motors.stop()

if __name__ == "__main__":

    while(True):

        collision_detection()

        key = getKey()
        d_logger.debug("Key %s pressed", key)
        if(key == 'c'):
            c.motors.stop()
            sys.exit(0)
        elif(key == 'w'):
            c.motors.setSpeedPercent(50)
            c.motors.moveForward()
        elif(key == 'W'):
            c.motors.setSpeedPercent(100)
            c.motors.moveForward()
        elif(key == 'a'):
            c.motors.setSpeedPercent(50)
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
