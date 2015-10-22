import time
import os
import sys
sys.path.insert(0, '../control')
from control import Control

c = Control()
stop_distance = 20

#Drive around em301
if  __name__ =='__main__':
	while(True):
		c.motors.setSpeedPercent(100)
		c.driveForwardUntilWall(30)
		c.driveBackwardUntilWall(30)
