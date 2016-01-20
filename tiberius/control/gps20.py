import serial
import sys
from enum import Enum

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


# class NMEASentence(Enum):
# 	GPGGA = "GPGGA"

class GlobalPositioningSystem:
    port = '/dev/ttyACM0'
    baud = 9600

    def __init__(self, debug=False):
        self.logger = logging.getLogger(
            'tiberius.control.GlobalPositioningSystem')
        self.logger.info('Creating an instance of GlobalPositioningSystem')
        self.ser = serial.Serial(self.port, self.baud, timeout=1)
        self.gpgga = nmea.GPGGA()
        self.gprmc = nmea.GPRMC()
        self.debug = debug

        # Accessible fields that can be directly accessed.
        self.latitude = None
        self.northsouth = None
        self.longitude = None
        self.eastwest = None
        self.attitude = None
        self.timestamp = None
        self.variation = None

        # if(self.s.isOpen()):
        # self.logger.info('GPS Serial port in open on ', port

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
            data = self.gpgga.parse(data)
            self.latitude = self.gpgga.latitude
            self.longitude = self.gpgga.longitude
        elif "GPRMC" in data:
            data = self.gprmc.parse(data)
            self.latitude = self.gprmc.lat
            self.longitude = self.gprmc.lon
        else:
            raise SentenceNotSupportedError(str(data))

    def update(self):
        try:
            self.__parse_data(self.__fetch_raw_data())
        except SentenceNotSupportedError:
            self.logger.warning("Receieved a bad sentence")

    def print_data(self):
        try:
            print 'Latitude: ', self.latitude
            print 'Longitude: ', self.longitude
        except AttributeError:
            self.logger.warning("Failed to print data")
        # print 'Altitude: ', self.gpgga.altitude

# For testing
import time
if __name__ == "__main__":
    gps = GlobalPositioningSystem()
    while(True):
        gps.update()
        gps.print_data()
        time.sleep(1)
