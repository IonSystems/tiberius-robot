import unittest
import sys
import socket
from tiberius.config.config_parser import TiberiusConfigParser

config = TiberiusConfigParser()

class ChangeIPAddress(unittest.TestCase):
    def runTest(self):
        original = config.getIPAddress()
        new = '10.8.8.21'
        config.setIPAddress(new)
        check = config.getIPAddress()
        self.assertEquals(new, check)
        return

class ValidIPAddress(unittest.TestCase):
    def runTest(self):
        ip_address = config.getIPAddress()
        try:
            socket.inet_aton(ip_address)
        except:
            self.fail("Invalid IP Address")
        return

class GetUltrasonicAddresses(unittest.TestCase):
    def runTest(self):
         rl = config.getUltrasonicRearLeftAddress()
         rr = config.getUltrasonicRearRightAddress()
         rc = config.getUltrasonicRearCentreAddress()
         fl = config.getUltrasonicFrontLeftAddress()
         fr = config.getUltrasonicFrontRightAddress()
         fc = config.getUltrasonicFrontCentreAddress()

         minAddress = 0
         maxAddress = 255

         self.assertTrue(isinstance(rl,(int, long)))
         self.assertTrue(isinstance(rr,(int, long)))
         self.assertTrue(isinstance(rc,(int, long)))
         self.assertTrue(isinstance(fl,(int, long)))
         self.assertTrue(isinstance(fr,(int, long)))
         self.assertTrue(isinstance(fc,(int, long)))

class GetSteeringType(unittest.TestCase):
    def runTest(self):
        st = config.getSteeringType()
        self.assertTrue(st == "Skid" or st == "Articulated" )

class CheckLidarValue(unittest.TestCase):
    def runTest(self):
        val = config.isLidarEnabled()
        self.assertTrue(isinstance(val, (bool)))

class CheckUnitName(unittest.TestCase):
    def runTest(self):
        val = config.getName()
        self.assertTrue(isinstance(val, (str)))
        #Max length based on specified max SSID length
        self.assertTrue(0 <= len(val) <= 32)

class CheckBatteryCapacity(unittest.TestCase):
    def runTest(self):
        val = long(config.getBatteryCapacity())
        self.assertTrue(isinstance(val, (int, long)))
        self.assertTrue(100 <= val <= 10000)

class CheckBatteryChemistry(unittest.TestCase):
    def runTest(self):
        val = config.getBatteryChemistry()
        self.assertTrue(val == "LiFe" or val == "LiPo" or val == "Lead")

class CheckLidarValue(unittest.TestCase):
    def runTest(self):
        val = config.isLidarEnabled()
        self.assertTrue(isinstance(val, (bool)))
