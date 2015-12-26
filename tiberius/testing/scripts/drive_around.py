import time
import os
import sys

from control.control import Control
from control import Control

c = Control()
stop_distance = 20



#Drive arounf em301
if  __name__ =='__main__':
	c.turnTo(-136)
	c.driveForwardUntilWall(30)
	c.turnRight90Degrees()
	c.turnLeft90Degrees()
	c.driveBackwardUntilWall(30)
