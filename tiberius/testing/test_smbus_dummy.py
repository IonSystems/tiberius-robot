import unittest
import sys
sys.path.insert(0, '../smbus_dummy')
from smbus import SMBus

bus = SMBus(1)

dev_addr = 0xB2
reg_addr = 0x00


class WriteReadWriteReadData(unittest.TestCase):

    def runTest(self):
        first = 92
        bus.write_byte_data(dev_addr, reg_addr, first)
        self.assertEquals(bus.read_byte_data(dev_addr, reg_addr), first)

        second = 71
        bus.write_byte_data(dev_addr, reg_addr, second)
        self.assertEquals(bus.read_byte_data(dev_addr, reg_addr), second)


class WriteReadData(unittest.TestCase):

    def runTest(self):
        #bus.write_byte_data(dev_addr, reg_addr, value)
        data = 255
        bus.write_byte_data(dev_addr, reg_addr, data)

        result = bus.read_byte_data(dev_addr, reg_addr)
        self.assertEquals(data, result)

if __name__ == "__main__":
    t = WriteReadWriteReadData()
    t.runTest()

    u = WriteData()
    u.runTest()
