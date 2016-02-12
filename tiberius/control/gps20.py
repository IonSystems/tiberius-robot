import serial
import sys
from enum import Enum

from tiberius.logger import logger
from tiberius.utils import detection

import logging
from pynmea import nmea

'''
    Reads GPS data. GPS data comes in many formats, we make use of a fraction of them at the moment.
'''


class SentenceNotSupportedError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class GlobalPositioningSystem:
    if detection.detect_windows():
        port = 'COM5'
    else:
        port = '/dev/ttyACM0'
    baud = 9600

    def __init__(self, debug=False):
        self.logger = logging.getLogger(
            'tiberius.control.GlobalPositioningSystem')
        self.logger.info('Creating an instance of GlobalPositioningSystem')
        self.ser = serial.Serial(self.port, self.baud, timeout=1)
        self.gpgga = nmea.GPGGA()
        self.gprmc = nmea.GPRMC()
        self.gpvtg = nmea.GPVTG()
        self.gpgsa = nmea.GPGSA()
        self.gpgll = nmea.GPGLL()

        self.debug = debug

        # Accessible fields that can be directly accessed.
        self.latitude = None
        self.longitude = None

        self.gps_qual = None
        self.num_sats = None
        self.dilution_of_precision = None
        self.velocity = None
        self.fixmode = None


        # if(self.s.isOpen()):
        # self.logger.info('GPS Serial port in open on ', port

    def __fetch_raw_data(self):
        try:
            self.ser.open()
        except:
            self.logger.warning("Serial port already open continuing.")
        data = self.ser.readline()
        self.logger.debug("Read data: " + data)
        self.ser.close()
        return data

    def __parse_data(self, data):
        if "GPGGA" in data:
            data = self.gpgga.parse(data)
            self.latitude = self.gpgga.latitude
            self.longitude = self.gpgga.longitude
            self.gls_qual = self.gpgga.gps_qual
            self.num_sats = self.gpgga.num_sats
            self.num_sats = self.gpgga.num_sats
            self.dilution_of_precision = self.gpgga.horizontal_dil
        elif "GPRMC" in data:
            data = self.gprmc.parse(data)
            self.latitude = self.gprmc.lat
            self.longitude = self.gprmc.lon
        elif "GPVTG" in data:
            data = self.gpvtg.parse(data)
            self.velocity = self.gpvtg.spd_over_grnd_kmph
        elif "GPGSA" in data:
            data = self.gpgsa.parse(data)
            self.fixmode = self.gpgsa.mode_fix_type
        elif "GPGLL" in data:
            data = self.gpgll.parse(data)
            self.latitude = self.gpgll.latitude
            self.longitude = self.gpgll.longitude
        else:
            raise SentenceNotSupportedError(str(data))

    def update(self):
        try:
            self.__parse_data(self.__fetch_raw_data())
        except SentenceNotSupportedError:
            self.logger.warning("Receieved a bad sentence")


    def read_gps(self):
        # Reads the gps a set number of times to ensure latest data
        for i in range(0, 5):
            self.update()

        return {'latitude': self.latitude, 'longitude': self.longitude, 'northsouth': self.northsouth,
                'eastwest': self.eastwest, 'altitude': self.altitude, 'variation': self.variation,
                'velocity': self.velocity}

    def has_fix(self):
        # Checks if there is a valid gps fix
        self.update()
        if self.fixmode > 0:  # we have a gps fix
            if self.latitude is not None and self.longitude is not None:
                return True
            else:
                return False


    def 

# For testing
import time

if __name__ == "__main__":
    gps = GlobalPositioningSystem()
    while True:
        gps.update()
        gps.print_data()
        time.sleep(1)
