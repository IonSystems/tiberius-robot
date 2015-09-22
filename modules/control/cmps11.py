#!/usr/bin/python

import smbus

class TiltCompensatedCompass:
	
	def __init__(self, address = 0x60):
		self.bus = smbus.SMBus(1)
		self.address = address

	hiby = 2
	loby = 3

	def heading(self):
		'''
			Get the heading valle between 0 and 3599.
		'''
		try:
			high_byte = self.bus.read_byte_data(self.address, self.hiby)
			low_byte = self.bus.read_byte_data(self.address, self.loby)
			#cmps11 returns two 8bits registers values
			#providing the range of 0-3599, representing 0 - 359.9 degrees
			return float((high_byte << 8) + low_byte)
		
		except IOError:
			print 'IO error cmps11'
			#attempt to get a value again
			high_byte = bus.read_byte_data(address,hiby)
			low_byte = bus.read_byte_data(address,loby)
			return float((high_byte << 8) + low_byte)

