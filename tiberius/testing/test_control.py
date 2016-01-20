import unittest
import time
import os
import sys
from tiberius.control.control import Control
c = Control()
stop_distance = 20


'''
	Control tests are designed to test control of the motors.
	Other sensors may be used to to ensure the correct operation of the motors.
'''


class DriveForwardUntilWall(unittest.TestCase):
    '''Drive forward in a straight line until an obsacle is detected from the front ultrasonic sensor.'''
    @unittest.skipUnless(os.uname()[4].startswith("arm"), "requires Raspberry Pi")
    def runTest(self):
        count = 0
        # Wait until Tiberius is 5cm away from the wall.
        while(c.frontNotHit(stop_distance)):
            c.motors.moveForward()
            time.sleep(0.1)
            count += 0.1
        c.motors.stop()
        # Cannot take any less than 3 seconds
        #self.assertGreater(count, 30)

        # Cannot take any more than 30 seconds
        #self.assertLess(count, 300)


class DriveBackwardUntilWall(unittest.TestCase):
    '''Drive backward in a straight line until an obsacle is detected from the front ultrasonic sensor.'''
    @unittest.skipUnless(os.uname()[4].startswith("arm"), "requires Raspberry Pi")
    def runTest(self):
        count = 0
        # Wait until Tiberius is 5cm away from the wall.
        while(c.rearNotHit(stop_distance)):
            c.motors.moveBackward()
            time.sleep(0.1)
            count += 0.1
        c.motors.stop()
        # Cannot take any less than 3 seconds
        #self.assertGreater(count, 30)

        # Cannot take any more than 30 seconds
        #self.assertLess(count, 300)


def turnTo(desired_bearing):
    while(True):

        actual_bearing = c.compass.headingNormalized()
        error = actual_bearing - desired_bearing
        print 'Heading: ' + str(actual_bearing)
        print 'Desired: ' + str(desired_bearing)

        if(error == 0):
            print 'At heading: ' + str(actual_bearing)
            c.motors.stop()
            break
        if(error > 180):
            print 'error > 180'
            error -= 360
        if(error < -180):
            print 'error < -180'
            error += 360
        if(error < 0):
            print 'error < 0 turning left'
            c.motors.turnLeft(50)
        else:
            print 'error > 0 turning right'
            c.motors.turnRight(50)
        print str(error)


class TurnRight90Degrees(unittest.TestCase):
    '''Turn on the spot, clockwise until Tiberius has rotated 90 degrees.'''
    @unittest.skipUnless(os.uname()[4].startswith("arm"), "requires Raspberry Pi")
    def runTest(self):
        old_bearing = c.compass.headingNormalized()

        desired_bearing = (old_bearing + 90)
        while(True):
            if(desired_bearing > 180):
                desired_bearing -= 360
            if(desired_bearing < -180):
                desired_bearing += 360
            if(desired_bearing > -180 and desired_bearing < 180):
                break
        print desired_bearing
        c.turnTo(desired_bearing)
        c.turnTo(desired_bearing)

        # Cannot take any less than 1 second
        #self.assertGreater(time, 10)

        # Cannot take any more than 6 seconds
        #self.assertLess(time, 60)


class TurnLeft90Degrees(unittest.TestCase):
    '''Turn on the spot, anti-clockwise until Tiberius has rotated 90 degrees.'''
    @unittest.skipUnless(os.uname()[4].startswith("arm"), "requires Raspberry Pi")
    def runTest(self):
        old_bearing = c.compass.headingNormalized()

        desired_bearing = (old_bearing - 90)
        while(True):
            if(desired_bearing > 180):
                desired_bearing -= 360
            if(desired_bearing < -180):
                desired_bearing += 360
            if(desired_bearing < 180 and desired_bearing > -180):
                break
        print desired_bearing
        c.turnTo(desired_bearing)
        c.turnTo(desired_bearing)
        # Cannot take any less than 1 second
        #self.assertGreater(time, 10)

        # Cannot take any more than 6 seconds
        # self.assertLess(time, 60


# For debugging
if __name__ == '__main__':
    try:
        # while(True):
        #		c.motors.turnLeft(50)
        d = TurnRight90Degrees()
        d.runTest()
    except KeyboardInterrupt:
        c.motors.stop()
        #d = TurnRight90Degrees()
        # d.runTest()
    # c.motors.turnRight(30)
    # time.sleep(1)

    # c.motors.stop()

#	while(True):
#		d = DriveForwardUntilWall()
#		d.runTest()
#		d = DriveBackwardUntilWall()
#		d.runTest()
