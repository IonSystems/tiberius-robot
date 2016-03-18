import sys
from tiberius.control.control import Control
from control import Control
c = Control()
if __name__ == "__main__":
    try:
        #		c.driveStraight(50,100)
        c.driveStraightStopStart(50, 100)
    except KeyboardInterrupt:
        c.motors.stop()
