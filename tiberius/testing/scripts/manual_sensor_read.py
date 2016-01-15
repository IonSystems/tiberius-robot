import sys
from tiberius.control.sensors import Ultrasonic
from tiberius.control.sensors import Compass
import time

if __name__ == "__main__":
	while(True):
		u = Ultrasonic()
		c = Compass()
		vals = u.senseUltrasonic()
		heading = c.headingNormalized()
		print str(vals)
		print str(heading)
		time.sleep(1)
