import unittest
import time

from control.control import Control

c = Control()
class DriveForwardUntilWall(unittest.TestCase):
	'''Drive forward in a straight line until an obsacle is detected from the front ultrasonic sensor.'''
	def runTest(self):
		time = 0
		#Wait until Tiberius is 5cm away from te wall.
		while(c.senseUltrasonic['fc'] > 5):
			c.moveForward()
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
