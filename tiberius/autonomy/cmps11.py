#!/usr/bin/python

import smbus

bus = smbus.SMBus(1)
address = 0x60
hiby = 2
loby = 3

def heading():
    try:
        high_byte = bus.read_byte_data(address,hiby)
        low_byte = bus.read_byte_data(address,loby)
        #cmps11 returns two 8bits registers values
        #providing the range of 0-3599
        return float((high_byte << 8) + low_byte)/10
    
    except IOError:
        print 'IO error cmps11'
        #attempt to get a value again
        high_byte = bus.read_byte_data(address,hiby)
        low_byte = bus.read_byte_data(address,loby)
        return float((high_byte << 8) + low_byte)/10
