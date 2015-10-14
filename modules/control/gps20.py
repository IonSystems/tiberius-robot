import serial
import logging
from pynmea import nmea

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
		self.ser.open()
		data = self.ser.readline()
		self.ser.close()
		return data

	def __parse_data(self, data):
		return self.gpgga.parse(data)

	def update(self):
		self.__parse_data(self.__fetch_raw_data())

	def print_data(self):
		print 'Latitude: ', self.gpgga.latitude
		print 'Longitude: ', self.gpgga.longitude
		#print 'Altitude: ', self.gpgga.altitude


#For testing
import time
if __name__ == "__main__":
	gps = GlobalPositioningSystem()
	while(True):
		gps.update()
		gps.print_data()
		time.sleep(1)

