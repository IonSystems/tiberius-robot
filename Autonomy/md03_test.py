#!/usr/bin/python

import smbus
import time

bus = smbus.SMBus(1)

for a in xrange(100,0,-10):
    bus.write_byte_data(0x58, 3, a)
    bus.write_byte_data(0x58, 2, 255)
    bus.write_byte_data(0x58, 0, 1)
    time.sleep(1)
    bus.write_byte_data(0x58, 2, 0)
    bus.write_byte_data(0x58, 0, 1)
    time.sleep(1)
