#!/usr/bin/python

import serial
from time import sleep
import json 

print "running"

class PowerManagement:

	# configure the serial connections (the parameters differs on the device you are connecting to)
	ser = serial.Serial(
    	port='/dev/ttyACM0',
    	baudrate=115200,
	)

	def getdata(self):
		data = ser.readline() #read(1000)  # read 9999 bytes of data. could use .readline() to get line of data
		dictionary = json.loads(data)
		return dictionary
		
	def testscript(self):
		while(1):
			data = ser.readline() #read(1000)  # read 9999 bytes of data. could use .readline() to get line of data
			if len(data) > 0:
        			print 'Got:', data
				dictionary = json.loads(data)
				#print dictionary
				monitor = dictionary["monitor"]
				volts = dictionary["volts"]
				current = dictionary["current"]
				power = dictionary["power"]
				time = dictionary["time"]
				amp_hours = dictionary["amp_hours"]
				watt_hours = dictionary["watt_hours"]
				print monitor
