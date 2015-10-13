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
		self.__gpgga = nmea.GPGGA()
		self.debug = debug

		#if(self.s.isOpen()):
			#self.logger.info('GPS Serial port in open on ', port

	def __fetch_gpgga_data(self):
		self.ser.open()
		data = ''
		timeout = 0
		while(not 'GPGGA' in data or timeout > 20):
			data = self.ser.readline()
			timeout += 1
		self.ser.close()
		return data

	def __parse_data(self, data):
		return self.__gpgga.parse(data)

	def update(self):
		raw = self.__fetch_gpgga_data()
		if self.debug:
			self.logger.debug(raw)
		self.__parse_data(raw)

	def print_data(self):
		print 'Timestam: ', self.__gpgga.timestamp
		print 'Latitude: ', self.__gpgga.latitude
		print 'Latitude Direction: ', self.__gpgga.lat_direction
		print 'Longitude: ', self.__gpgga.longitude
		print 'Longitude Direction: ', self.__gpgga.lon_direction
		print 'GPS Quality Indicator: ', self.__gpgga.gps_qual
		print 'Number of Satillites: ', self.__gpgga.num_sats
		print 'Horizontal Dilution of Precision: ', self.__gpgga.horizontal_dil
		print 'Antenna altitude above sea level (mean): ', self.__gpgga.antenna_altitude
		print 'Units of altitude (meters):', self.__gpgga.altitude_units
		print 'Geoidal Seperation: ', self.__gpgga.geo_sep
		print 'Units of Geoidal Seperation: ', self.__gpgga.geo_sep_units
		#print 'Age of Differential GPS Data (sec): ', self.__gpgga.age_gps_data
		#print 'Differential Reference Station ID: ', self.__gpgga.ref_station_id


	def get_data_object(self):
		return self.__gpgga
#For testing
import time
if __name__ == "__main__":
	gps = GlobalPositioningSystem()
	while(True):
		gps.update()
		gps.print_data()
		time.sleep(1)

