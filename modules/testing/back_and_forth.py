import time
import os

#TODO: rename module or something
from control.control import Control

c = Control()
stop_distance = 20



#Drive arounf em301
if  __name__ =='__main__':
	while(True):
		c.driveForwardUntilWall(30,100)	
		c.driveBackwardUntilWall(30,100)
