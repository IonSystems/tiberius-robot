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
        port = 'COM3'
    else:
        port = '/dev/ttyACM0'
    baud = 9600

    supported_sentences = 3  # The number of NMEA sentences currently supported
    invalid_sentences_count = 100  # The number of invalid sentences to accept before stopping

    def __init__(self, debug=False):
        self.logger = logging.getLogger(
            'tiberius.control.GlobalPositioningSystem')
        self.logger.info('Creating an instance of GlobalPositioningSystem')
        self.ser = serial.Serial(self.port, self.baud, timeout=1)
        self.gpgga = nmea.GPGGA()
        self.gpvtg = nmea.GPVTG()
        self.gpgsa = nmea.GPGSA()


        self.debug = debug

        # Accessible fields that can be directly accessed.
        self.latitude = None
        self.longitude = None

        self.gps_qual = None
        self.num_sats = None
        self.dilution_of_precision = None
        self.velocity = None
        self.fixmode = None


    def fetch_raw_data(self):
        try:
            self.ser.open()
        except:
            self.logger.warning("Serial port already open continuing.")
        data = self.ser.readline()
        if self.debug:
            self.logger.debug("Read data: " + data)
        self.ser.close()
        return data

    def parse_data(self, data):
        if "GPGGA" in data:
            data = self.gpgga.parse(data)
            self.latitude = self.gpgga.latitude
            self.longitude = self.gpgga.longitude
            self.gls_qual = self.gpgga.gps_qual
            self.num_sats = self.gpgga.num_sats
            self.num_sats = self.gpgga.num_sats
            self.dilution_of_precision = self.gpgga.horizontal_dil

        elif "GPVTG" in data:
            data = self.gpvtg.parse(data)
            self.velocity = self.gpvtg.spd_over_grnd_kmph

        elif "GPGSA" in data:
            data = self.gpgsa.parse(data)
            self.fixmode = self.gpgsa.mode_fix_type

        else:
            return False
        if self.latitude is not None:
            if self.latitude is str:
                if self.latitude.startswith("00"):
                    self.latitude = self.latitude[2:]
                    self.latitude = "-" + self.latitude
                    if self.debug:
                        print self.latitude
            if self.longitude is str:
                if self.longitude.startswith("00"):
                    self.longitude = self.longitude[2:]
                    self.longitude = "-" + self.longitude
                    if self.debug:
                        print self.longitude

            if self.latitude is not "":
                self.latitude = float(self.latitude)
                self.latitude /= 100
            else:
                if self.debug:
                        print 'No data in latitude'
            if self.longitude is not "":
                self.longitude = float(self.longitude)
                self.longitude /= 100
            else:
                if self.debug:
                        print 'No Data in longitude'
        return True

    def update(self):
        # Reads the gps a set number of times to ensure latest data
        for i in range(0, self.invalid_sentences_count):
            if self.parse_data(self.fetch_raw_data()):
                break
                return True
        return False

    def read_gps(self):
        successful_sentences = 0
        for i in range(0, self.supported_sentences):  # Query for the number of sentences to ensure we get latest data
            if self.update():
                successful_sentences += 1
        if successful_sentences < self.supported_sentences:
            return False

        return {'latitude': self.latitude, 'longitude': self.longitude, 'gls_qual': self.gps_qual,
                'num_sats': self.num_sats, 'dilution_of_precision': self.dilution_of_precision,
                'velocity': self.velocity, 'fixmode': self.fixmode}

    def has_fix(self):
        # Checks if there is a valid gps fix
        self.update()
        if self.fixmode > 0:  # we have a gps fix
            if self.latitude is not None and self.longitude is not None:
                return True
            else:
                return False

# For testing
import time

if __name__ == "__main__":
    gps = GlobalPositioningSystem()
    while True:
        gps.update()
        # gps.print_data()
        time.sleep(1)
