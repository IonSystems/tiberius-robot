import unittest
import sys
import socket
import tiberius.config.config_parser
from tiberius.config.config_parser import TiberiusConfigParser


class ChangeIPAddress(unittest.TestCase):

    def runTest(self):
        original = TiberiusConfigParser.getIPAddress()
        new = '10.8.8.21'
        TiberiusConfigParser.setIPAddress(new)
        check = TiberiusConfigParser.getIPAddress()
        self.assertEquals(new, check)
        return


class ValidIPAddress(unittest.TestCase):

    def runTest(self):
        ip_address = TiberiusConfigParser.getIPAddress()
        try:
            socket.inet_aton(ip_address)
        except:
            self.fail("Invalid IP Address")
        return


class GetUltrasonicAddresses(unittest.TestCase):

    def runTest(self):
        rl = TiberiusConfigParser.getUltrasonicRearLeftAddress()
        rr = TiberiusConfigParser.getUltrasonicRearRightAddress()
        rc = TiberiusConfigParser.getUltrasonicRearCentreAddress()
        fl = TiberiusConfigParser.getUltrasonicFrontLeftAddress()
        fr = TiberiusConfigParser.getUltrasonicFrontRightAddress()
        fc = TiberiusConfigParser.getUltrasonicFrontCentreAddress()

        minAddress = 0
        maxAddress = 255

        self.assertTrue(isinstance(rl, (int, long)))
        self.assertTrue(isinstance(rr, (int, long)))
        self.assertTrue(isinstance(rc, (int, long)))
        self.assertTrue(isinstance(fl, (int, long)))
        self.assertTrue(isinstance(fr, (int, long)))
        self.assertTrue(isinstance(fc, (int, long)))


class GetCompassAddress(unittest.TestCase):

    def runTest(self):
        addr = TiberiusConfigParser.getCompassAddress()

        minAddress = 0
        maxAddress = 255

        self.assertTrue(isinstance(addr, (int, long)))


class GetSteeringType(unittest.TestCase):

    def runTest(self):
        st = TiberiusConfigParser.getSteeringType()
        self.assertTrue(st == "Skid" or st == "Articulated")


class CheckLidarValue(unittest.TestCase):

    def runTest(self):
        val = TiberiusConfigParser.isLidarEnabled()
        self.assertTrue(isinstance(val, (bool)))


class CheckUnitName(unittest.TestCase):

    def runTest(self):
        val = TiberiusConfigParser.getName()
        self.assertTrue(isinstance(val, (str)))
        # Max length based on specified max SSID length
        self.assertTrue(0 <= len(val) <= 32)


class CheckBatteryCapacity(unittest.TestCase):

    def runTest(self):
        val = long(TiberiusConfigParser.getBatteryCapacity())
        self.assertTrue(isinstance(val, (int, long)))
        self.assertTrue(100 <= val <= 10000)


class CheckBatteryChemistry(unittest.TestCase):

    def runTest(self):
        val = TiberiusConfigParser.getBatteryChemistry()
        self.assertTrue(val == "LiFe" or val == "LiPo" or val == "Lead")


class CheckLidarValue(unittest.TestCase):

    def runTest(self):
        val = TiberiusConfigParser.isLidarEnabled()
        self.assertTrue(isinstance(val, (bool)))

if __name__ == "__main__":
    unittest.main()
