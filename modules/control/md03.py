#!/usr/bin/python

import smbus
import sys
sys.path.insert(0, '../logger')
#import logger.logger as logger
from logger import logger as logger
import logging

class MotorDriver:
	'''Motor Driver'''

	def __init__(self, address, debug=False, inverted = False):
		self.logger = logging.getLogger('tiberius.control.MotorDriver')
		self.logger.info('Creating an instance of MotorDriver')

		self.bus = smbus.SMBus(1)
		self.address = address
		self.debug = debug
		self.inverted = inverted

		self.current_register = 0x05
		self.status_register = 0x01

	'''Returns a current value between 0(0A) and 186(20A)'''
	def current(self):
		current = self.bus.read_byte_data(self.address, self.current_register)
		amps = round(((current / 186.0) * 20.0), 3)
		return amps

	'''	Returns the status register bits:
		0: Acceleration in progress LSB
		1: Over-current indicator
		2: Over-temperature indicator
		The bits are returned in dictionary form.
	'''
	def status(self):
		status = self.bus.read_byte_data(self.address, self.status_register)
		return status
		#print str(status)
		#accel = status & 1
		#over-current = (status >> 1) & 1
		#over-temp = (stats >> 2) & 1
#return {'accel' : accel, 'over-current' : over-current, 'over-temp' : over-temp}
	def check_range(self, min, max, val):
		if val > max:
			return 1
		elif val < min:
			return -1
		return 0

	def speed_restrict(self, speed):
		r = self.check_range(-255, 255, speed)
		if r > 0:
			speed = 255
			self.logger.warn('Speed parameter out of range.')
		elif r < 0:
			speed = -255
			self.logger.warn('Speed parameter out of range.')
		return speed

		def accel_restrict(self, accel):
			r = self.check_range(0, 255, accel)
			if r > 0:
				accel = 255
				self.logger.warn('Acceleration parameter out of range.')
			elif r < 0:
				accel = 0
				self.logger.warn('Acceleration parameter out of range.')
			return accel

	def move(self, speed, accel):
		try:
			if ((speed<-255) or (speed>255)):
				print 'Speed parameter out of range.'
				return 0

			if ((accel<0) or (accel>255)):
				print 'Acceleration parameter out of range.'
				return 0

			self.bus.write_byte_data(self.address,3,accel)
			if (speed>=0):
				if (self.debug): print speed
				self.bus.write_byte_data(self.address,2,int(speed))
				#the way the motors are installed on the robot
				#0x59 and 0x5B go forward when receive reverse command
				if ((self.address==0x58) or (self.address==0x5A)):
					self.bus.write_byte_data(self.address,0,1)
				if ((self.address==0x59) or (self.address==0x5B)):
					self.bus.write_byte_data(self.address,0,2)
			if (speed<0):
				if (self.debug): print speed
				self.bus.write_byte_data(self.address,2,int(-speed))
				if ((self.address==0x58) or (self.address==0x5A)):
					self.bus.write_byte_data(self.address,0,2)
				if ((self.address==0x59) or (self.address==0x5B)):
					self.bus.write_byte_data(self.address,0,1)
			return 1

		except IOError, e:
			self.logger.warn('IO error on I2C bus, address %s (%s)', hex(self.address), e)
