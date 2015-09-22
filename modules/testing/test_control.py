import unittest
import time
import os
from control.control import Control

c = Control()

'''
	Control tests are designed to test control of the motors.
	Other sensors may be used to to ensure the correct operation of the motors.
'''

class DriveForwardUntilWall(unittest.TestCase):
	'''Drive forward in a straight line until an obsacle is detected from the front ultrasonic sensor.'''
	@unittest.skipUnless(os.uname()[4].startsWith("arm") , "requires Raspberry Pi")
	def runTest(self):
		if not is_raspberry_pi():
			self.skip
		time = 0
		#Wait until Tiberius is 5cm away from the wall.
		while(c.senseUltrasonic['fc'] > 5):
			c.moveForward()
			sleep(1)
			time += 1

		#Cannot take any less than 3 seconds
		self.assertGreater(time, 3)

		#Cannot take any more than 30 seconds
		self.assertLess(time, 30)
		
class DriveBackwardUntilWall(unittest.TestCase):
	'''Drive backward in a straight line until an obsacle is detected from the front ultrasonic sensor.'''
	@unittest.skipUnless(os.uname()[4].startsWith("arm") , "requires Raspberry Pi")
	def runTest(self):
		time = 0
		#Wait until Tiberius is 5cm away from the wall.
		while(c.senseUltrasonic['rc'] > 5):
			c.moveBackward()
			sleep(1)
			time += 1

		#Cannot take any less than 3 seconds
		self.assertGreater(time, 3)

		#Cannot take any more than 30 seconds
		self.assertLess(time, 30)


#For debugging
if  __name__ =='__main__':
    c = TestMotorsAndUltrasonic()
    c.runTest()
