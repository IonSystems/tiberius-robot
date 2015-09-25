from control.control import Control
import time

if __name__ == "__main__":
	while(True):
		c = Control()
		vals = c.senseUltrasonic()
		print str(vals)
		time.sleep(1)
	
