import sys
from tiberius.control.control import Control
c = Control()
if __name__ == "__main__":
    try:
        c.driveStraight(50, 12)  # 50% speed for 11.5s
        c.turnLeft90Degrees()
        c.driveStraight(40, 10)

    except KeyboardInterrupt:
        c.motors.stop()
