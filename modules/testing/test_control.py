import unittest
import time
import os
from control.control import Control

c = Control()
stop_distance = 20


class DriveForwardUntilWall(unittest.TestCase):
	'''Drive forward in a straight line until an obsacle is detected from the front ultrasonic sensor.'''
	@unittest.skipUnless(os.uname()[4].startswith("arm") , "requires Raspberry Pi")
	def runTest(self):
		count = 0
		#Wait until Tiberius is 5cm away from the wall.
		while(c.frontNotHit(stop_distance)):
			c.moveForward()
			time.sleep(1)
			count += 1
		c.stop()
		#Cannot take any less than 3 seconds
		self.assertGreater(count, 3)

		#Cannot take any more than 30 seconds
		self.assertLess(count, 30)
		
class DriveBackwardUntilWall(unittest.TestCase):
	'''Drive backward in a straight line until an obsacle is detected from the front ultrasonic sensor.'''
	@unittest.skipUnless(os.uname()[4].startswith("arm") , "requires Raspberry Pi")
	def runTest(self):
		count = 0
		#Wait until Tiberius is 5cm away from the wall.
		while(c.rearNotHit(stop_distance)):
			c.moveBackward()
			time.sleep(1)
			count += 1
		c.stop()
		#Cannot take any less than 3 seconds
		self.assertGreater(count, 3)

		#Cannot take any more than 30 seconds
		self.assertLess(count, 30)


#For debugging
if  __name__ =='__main__':
    d = DriveForwardUntilWall()
    d = DriveBackwardUntilWall()
    d.runTest()
