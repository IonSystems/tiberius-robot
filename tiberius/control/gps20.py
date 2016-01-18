import serial
import sys
from tiberius.logger import logger
#import logger.logger as logger

import logging
from pynmea import nmea
'''
	Reads GPS data. GPS data comes in many formats, currently we are only interested
	in the NMEA GPGGA sentences (Global Positioning System Fix Data).


'''
class SentenceNotSupportedError(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

class GlobalPositioningSystem:
	port = '/dev/ttyACM0'
	baud = 9600

	def __init__(self, debug=False):
		self.logger = logging.getLogger('tiberius.control.GlobalPositioningSystem')
		self.logger.info('Creating an instance of GlobalPositioningSystem')
		self.ser = serial.Serial(self.port, self.baud, timeout = 1)
		self.gpgga = nmea.GPGGA()
		self.debug = debug

		#if(self.s.isOpen()):
			#self.logger.info('GPS Serial port in open on ', port

	def __fetch_raw_data(self):
		try:
			self.ser.open()
		except:
			self.logger.warning("Serial port already open continueing.")
		data = self.ser.readline()
		self.logger.debug("Read data: " + data)
		self.ser.close()
		return data

	def __parse_data(self, data):
		if "GPGGA" in data:
			return self.gpgga.parse(data)
		else:
			raise SentenceNotSupportedError(str(data))

	def update(self):
		try:
			self.__parse_data(self.__fetch_raw_data())
		except SentenceNotSupportedError:
			self.logger.warning("Receieved a bad sentence")

	def print_data(self):
		try:
			print 'Latitude: ', self.gpgga.latitude
			print 'Longitude: ', self.gpgga.longitude
		except AttributeError:
			self.logger.warning("Failed to print data")	
		#print 'Altitude: ', self.gpgga.altitude

	def find_dev_path(self):
		return		
#For testing
import time
if __name__ == "__main__":
	gps = GlobalPositioningSystem()
	while(True):
		gps.update()
		gps.print_data()
		time.sleep(1)
