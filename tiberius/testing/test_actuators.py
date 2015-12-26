import unittest
import sys
import os
from tiberius.control.actuators import Motor
m = Motor()

class TestSetSpeedPercent(unittest.TestCase):
    @unittest.skipUnless(os.uname()[4].startswith("arm") , "requires Raspberry Pi")
    def runTest(self):
        m.setSpeedPercent(100)
        self.assertEquals(255, m.speed)
        m.setSpeedPercent(0)
        self.assertEquals(0, m.speed)
        m.setSpeedPercent(50)
        self.assertEquals(255/2, m.speed)

class TestStop(unittest.TestCase):
    @unittest.skipUnless(os.uname()[4].startswith("arm") , "requires Raspberry Pi")
    def runTest(self):
        m.stop()
        #Ensure speed of all the motors is zero
        self.assertEquals(0,m.front_left.speed())
        self.assertEquals(0,m.front_right.speed())
        self.assertEquals(0,m.rear_left.speed())
        self.assertEquals(0,m.rear_right.speed())

class TestMoveForward(unittest.TestCase):
    @unittest.skipUnless(os.uname()[4].startswith("arm") , "requires Raspberry Pi")
    def runTest(self):
        m.moveForward()
        self.assertEquals(255,m.front_left.speed())
        self.assertEquals(255,m.front_right.speed())
        self.assertEquals(255,m.rear_left.speed())
        self.assertEquals(255,m.rear_right.speed())

class TestMoveBackward(unittest.TestCase):
    @unittest.skipUnless(os.uname()[4].startswith("arm") , "requires Raspberry Pi")
    def runTest(self):
        m.moveBackward()
        self.assertEquals(255,m.front_left.speed())
        self.assertEquals(255,m.front_right.speed())
        self.assertEquals(255,m.rear_left.speed())
        self.assertEquals(255,m.rear_right.speed())

class TestTurnRight(unittest.TestCase):
    @unittest.skipUnless(os.uname()[4].startswith("arm") , "requires Raspberry Pi")
    def runTest(self):
        m.turnRight()
        self.assertEquals(255,m.front_left.speed())
        self.assertEquals(255,m.front_right.speed())
        self.assertEquals(255,m.rear_left.speed())
        self.assertEquals(255,m.rear_right.speed())

class TestTurnLeft(unittest.TestCase):
    @unittest.skipUnless(os.uname()[4].startswith("arm") , "requires Raspberry Pi")
    def runTest(self):
        m.turnLeft()
        self.assertEquals(255,m.front_left.speed())
        self.assertEquals(255,m.front_right.speed())
        self.assertEquals(255,m.rear_left.speed())
        self.assertEquals(255,m.rear_right.speed())


class TestMoveForwardDualSpeed(unittest.TestCase):
    @unittest.skipUnless(os.uname()[4].startswith("arm") , "requires Raspberry Pi")
    def runTest(self):
        m.moveForwardDualSpeed(34, 43)
        self.assertEquals(34,m.front_left.speed())
        self.assertEquals(43,m.front_right.speed())
        self.assertEquals(34,m.rear_left.speed())
        self.assertEquals(43,m.rear_right.speed())

class TestMoveIndependantSpeeds(unittest.TestCase):
    @unittest.skipUnless(os.uname()[4].startswith("arm") , "requires Raspberry Pi")
    def runTest(self):
        m.moveIndependentSpeeds(10,11,12,13)
        self.assertEquals(10,m.front_left.speed())
        self.assertEquals(11,m.front_right.speed())
        self.assertEquals(12,m.rear_left.speed())
        self.assertEquals(13,m.rear_right.speed())

class TestClipSpeedValue(unittest.TestCase):
    @unittest.skipUnless(os.uname()[4].startswith("arm") , "requires Raspberry Pi")
    def runTest(self):
        v = m._Motor__clipSpeedValue(-8787)
        self.assertEquals(v, -255)

        v = m._Motor__clipSpeedValue(0)
        self.assertEquals(v, 0)

        v = m._Motor__clipSpeedValue(9999)
        self.assertEquals(v, 255)

        v = m._Motor__clipSpeedValue(255)
        self.assertEquals(v, 255)

        v = m._Motor__clipSpeedValue(-255)
        self.assertEquals(v, -255)
