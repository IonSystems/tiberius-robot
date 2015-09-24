import unittest
import time
import os

#TODO: rename module or something
from control.control import Control

c = Control()
stop_distance = 20


'''
	Control tests are designed to test control of the motors.
	Other sensors may be used to to ensure the correct operation of the motors.
'''

class DriveForwardUntilWall(unittest.TestCase):
	'''Drive forward in a straight line until an obsacle is detected from the front ultrasonic sensor.'''
	@unittest.skipUnless(os.uname()[4].startswith("arm") , "requires Raspberry Pi")
	def runTest(self):
		count = 0
		#Wait until Tiberius is 5cm away from the wall.
		while(c.frontNotHit(stop_distance)):
			c.motors.moveForward()
			time.sleep(0.1)
			count += 0.1
		c.motors.stop()
		#Cannot take any less than 3 seconds
		self.assertGreater(count, 30)

		#Cannot take any more than 30 seconds
		self.assertLess(count, 300)
		
class DriveBackwardUntilWall(unittest.TestCase):
	'''Drive backward in a straight line until an obsacle is detected from the front ultrasonic sensor.'''
	@unittest.skipUnless(os.uname()[4].startswith("arm") , "requires Raspberry Pi")
	def runTest(self):
		count = 0
		#Wait until Tiberius is 5cm away from the wall.
		while(c.rearNotHit(stop_distance)):
			c.motors.moveBackward()
			time.sleep(0.1)
			count += 0.1
		c.motors.stop()
		#Cannot take any less than 3 seconds
		self.assertGreater(count, 30)

		#Cannot take any more than 30 seconds
		self.assertLess(count, 300)
		
class TurnToRight90Degrees(unittest.TestCase):
	'''Turn on the spot, clockwise until Tiberius has rotated 90 degrees.'''
	@unittest.skipUnless(os.uname()[4].startswith("arm") , "requires Raspberry Pi")
	def runTest(self):
		old_bearing = c.compass.headingDegrees()

		desired_bearing = (old_bearing + 90) % 360

		#Wait until tiberius has rotated 90 degrees
		c.motors.turnRight()
		while(c.compass.headingDegrees() < desired_bearing):
			time = 0
			sleep(0.1)
			time += 0.1
		c.motors.stop()
		#Cannot take any less than 3 seconds
		self.assertGreater(time, 1)

		#Cannot take any more than 30 seconds
		self.assertLess(time, 30)
		
class TurnToLeft90Degrees(unittest.TestCase):
	'''Turn on the spot, anti-clockwise until Tiberius has rotated 90 degrees.'''
	@unittest.skipUnless(os.uname()[4].startswith("arm") , "requires Raspberry Pi")
	def runTest(self):
		old_bearing = c.compass.headingDegrees()

		desired_bearing = (old_bearing + 90) % 360

		#Wait until tiberius has rotated 90 degrees
		c.motors.turnLeft()
		while(c.compass.headingDegrees() < desired_bearing):
			time = 0
			sleep(0.1)
			time += 0.1
		c.motors.stop()

		#Cannot take any less than 3 seconds
		self.assertGreater(time, 1)

		#Cannot take any more than 30 seconds
		self.assertLess(time, 30)


#For debugging
if  __name__ =='__main__':
    d = DriveForwardUntilWall()
    d = DriveBackwardUntilWall()
    d.runTest()
    c = DriveBackwardUntilWall()
    c.runTest()
