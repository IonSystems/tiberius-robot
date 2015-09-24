import time
import os
import sys

#TODO: rename module or something
from control.control import Control

c = Control()
stop_distance = 20



#Drive around em301
if  __name__ =='__main__':
	while(True):
		try:
			c.driveForwardUntilWall(30,100)	
			c.driveBackwardUntilWall(30,100)
		except KeyboardInterrupt:
			c.motors.stop()
			sys.exit(0)
