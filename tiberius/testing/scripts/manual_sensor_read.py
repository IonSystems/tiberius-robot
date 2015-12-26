import sys
from tiberius.control.control import Control

from control import Control
import time

if __name__ == "__main__":
	while(True):
		c = Control()
		vals = c.ultrasonics.senseUltrasonic()
		heading = c.compass.headingNormalized()
		print str(vals)
		print str(heading)
		time.sleep(1)
