#!/usr/bin/python

import smbus

class TiltCompensatedCompass:
	
	def __init__(self, address = 0x60):
		self.bus = smbus.SMBus(1)
		self.address = address
	__heading = -1
	__heading_degrees = -1

	hiby = 2
	loby = 3

	#Store most recent heading for fetching
	
	def __read(self):
		#print 'Reading'
		#cmps11 returns two 8bits registers values
		#providing the range of 0-3599, representing 0 - 359.9 degrees
		high_byte = self.bus.read_byte_data(self.address, self.hiby)
		low_byte = self.bus.read_byte_data(self.address, self.loby)
		self.__heading = float((high_byte << 8) + low_byte)
		self.__heading_degrees = self.__heading / 10
		return self.__heading

	def getMostRecentDegrees(self):
		#if self.__heading_degrees < 0:
		#	return False
		return self.__heading_degrees

	def heading(self):
		'''
			Get the heading value between 0 and 3599.
		'''
		while(True):

			try:
				heading = self.__read()	
				return heading	
			except IOError:
				print 'Error reading compass'
