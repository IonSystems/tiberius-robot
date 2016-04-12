import serial
import sys
import logging
import time

from pynmea import nmea
from tiberius.logger import logger
from tiberius.utils import detection
from tiberius.config.config_parser import TiberiusConfigParser


class GlobalPositioningSystem:
    '''
    Reads GPS data.
    GPS data comes in many formats. We parse the most useful senstences for
    our needs and ignore the rest.

    The serial port must be correctly set in the config file for successful
    communication.

    The publically accessible functions allow access to the most recent GPS
    data, and allow to check if there is a current fix. Fields and the remainder
    of the functions have been hidden to prevent misuse of the class. E.g
    externally changing fields, or accidentally calling the wrong function.
    '''
    if detection.detect_windows():
        port = 'COM3'
    else:
        port = TiberiusConfigParser.getGPSSerialPort()
    baud = 9600

    def __init__(self, debug=False):
        self.logger = logging.getLogger(
            'tiberius.control.GlobalPositioningSystem')
        self.logger.info('Creating an instance of GlobalPositioningSystem')
        self.ser = serial.Serial(self.port, self.baud, timeout=1)

        # Each GP* instance is used to decode the matching raw sentence.
        self.__gpgga = nmea.GPGGA()
        self.__gpvtg = nmea.GPVTG()
        self.__gpgsa = nmea.GPGSA()
        self.__gprmc = nmea.GPRMC()

        self.debug = debug
        ''' Set debug to true to enable addition print outs.'''

        self.__latitude = -1.0
        self.__longitude = -1.0

        self.__gps_qual = -1
        self.__num_sats = -1
        self.__dilution_of_precision = -1
        self.__velocity = -1
        self.__fixmode = None
        self.__timestamp = None

    def read_gps(self):
        '''
        When this function is called, a singular GPS sentence is read and saved
        to our fields. A portion of these fields are then returned.

        Return a dictionary containing:
            - latitude
            - longitude
            - GPS quality
            - number of satilites
            - dilution of precision
            - velocity
            - fix quality

        :note: Due to the nature of how we collect GPS data, different values
        may have been read at different times, but we make the assumption that
        data arrives often enough that it is not a big issue.

        All of the above just happen to be exactly what we store in the
        database.
        '''
        self.__update()
        results = {
            'latitude': self.__latitude,
            'longitude': self.__longitude,
            'gps_qual': self.__gps_qual,
            'num_sats': self.__num_sats,
            'dilution_of_precision': self.__dilution_of_precision,
            'velocity': self.__velocity,
            'fixmode': self.__fixmode,
            'timestamp': self.__timestamp
        }

        return results

    def usable(self):
        # Checks if there is a valid gps fix
        self.__update()
        fix = self.__has_fix()
        pos = self.__has_pos()
        rec = self.__is_recent()
        usable = fix and pos and rec
        if not usable:
            status = "Fix: " + str(fix) + ", Pos: " + str(pos) + ", Recent: " + str(rec)
            self.logger.warning("Data not usable: (%s)", status)
        return usable

    '''***********************************
            Hidden Functions
    ***********************************'''

    def __has_fix(self):
        return self.__fixmode > 0

    def __has_pos(self):
        return (self.__latitude and self.__longitude)

    def __is_recent(self):
        # Units are seconds
        age = time.time() - self.__timestamp
        return age < 5

    def __fetch_raw_data(self):
        try:
            self.ser.open()
        except:
            self.logger.warning("Serial port already open continuing.")
        data = self.ser.readline()
        if self.debug:
            self.logger.debug("Read data: " + data)
        self.ser.close()
        return data

    def __update(self):
        # Reads the gps a set number of times to ensure latest data
        return self.__parse_data(self.__fetch_raw_data())

    def __parse_data(self, data):
        '''
        Extract data items from raw NMEA sentences and update the values
        stored in the fields.

        .. note:: Only the following NMEA senstences are supported:
            - GPGGA
            - GPVTG
            - GPGSA
            - GPRMC

        :note: Previously the timestamp was generated further on in the call
        stack. But it seems more appropriate to record the timestamp as close
        to the capture time as possible, hence why we not record the timestamp
        here. Also we purposely only update the timestamp if we get a new
        latitude and longitude, because those are the most valuable members.

        :return: True if a sentence is parsed succesfully, False otherwise.
        '''
        if "GPGGA" in data:
            data = self.__gpgga.parse(data)
            self.__latitude = self.__parse_lat(self.__gpgga.latitude)
            self.__longitude = self.__parse_long(self.__gpgga.longitude)
            self.__gps_qual = self.__gpgga.gps_qual
            self.__num_sats = self.__gpgga.num_sats
            self.__num_sats = self.__gpgga.num_sats
            self.__dilution_of_precision = self.__gpgga.horizontal_dil
            self.__fixmode = self.__gpgga.gps_qual
            self.__timestamp = time.time()

        elif "GPVTG" in data:
            data = self.__gpvtg.parse(data)
            self.__velocity = self.__gpvtg.spd_over_grnd_kmph

        elif "GPGSA" in data:
            data = self.__gpgsa.parse(data)
            self.__fixmode = self.__gpgsa.mode_fix_type

        elif "GPRMC" in data:
            data = self.__gprmc.parse(data)
            self.__latitude = self.__parse_lat(self.__gprmc.lat)
            self.__longitude = self.__parse_long(self.__gprmc.lon)
            # We NEED to set fixmode
            if self.__gprmc.data_validity == 'A':
                self.__fixmode = 1
            self.__timestamp = time.time()

        else:
            return False
        return True

    def __parse_long(longitude):
        '''
        Convert the NMEA string into a valid floating point representation.
        '''
        longitude = float(longitude[3:])/60+float(longitude[:3])
        return longitude

    def __parse_lat(latitude):
        '''
        Convert the NMEA string into a valid floating point representation.
        '''
        latitude = float(latitude[2:])/60+float(latitude[:2])
        return latitude

# For testing
import time

if __name__ == "__main__":
    gps = GlobalPositioningSystem(debug=True)
    while True:
        #print gps.__fetch_raw_data()
        #gps.has_fix()
        print gps.read_gps()
        #print "LAT:" + str(gps.latitude)
        time.sleep(0.1)
