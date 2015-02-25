#!/usr/bin/python

import smbus
import time


for a in xrange(0,30):
    bus = smbus.SMBus(1)
    time.sleep(1.5)
    bus.write_byte_data(0x70,2,170)
    bus.write_byte_data(0x70,1,19)
    bus.write_byte_data(0x70,0,81)
    time.sleep(0.07)
    hiby = bus.read_byte_data(0x70,2)
    loby = bus.read_byte_data(0x70,3)
    result = (hiby<<8)+loby
    print 'loby is {} and hiby is {}'.format(loby,hiby)
