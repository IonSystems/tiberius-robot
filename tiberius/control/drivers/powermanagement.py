#!/usr/bin/python

import serial
from time import sleep
import json
from tiberius.config.config_parser import TiberiusConfigParser

print "running"

class PowerManagement:

	# configure the serial connections (the parameters differs on the device you are connecting to)

	mbedport =TiberiusConfigParser.getBatteryMonitorPort()
	ser = serial.Serial(
    	port= mbedport,
    	baudrate=115200,
	)

	def getdata(self):
		data =self.ser.readline() #read(1000)  # read 9999 bytes of data. could use .readline() to get line of data
		try: #TODO: should not recursively call getdata when it goes wrong.
			dictionary = json.loads(data)
			if dictionary is not None:
				return dictionary
			else:
				return self.getdata()
		except:
			return self.getdata()


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
