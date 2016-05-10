#!/usr/bin/python

import serial
from time import sleep

print "running"

# configure the serial connections (the parameters differs on the device you are connecting to)
ser = serial.Serial(
    port='/dev/ttyACM0',
    baudrate=115200,
)

while(1):
	print "happening once"
	data = ser.readline() #read(1000)  # read 9999 bytes of data. could use .readline() to get line of data
	if len(data) > 0:
        	print 'Got:', data


