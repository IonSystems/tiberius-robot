#!/usr/bin/python
import time
import logging
from tiberius.logger import logger
from tiberius.utils import detection
# If not running on a raspberry pi, use the dummy smbus library to allow
# simulation of I2C transactions.
if not detection.detect_pi():
    from tiberius.smbus_dummy import smbus
else:
    import smbus


class UltrasonicRangefinder:
    '''Ultrasonic rangefinder'''

    # parameters
    commandreg = 0x00
    gainreg = 0x01
    rangereg = 0x02

    # Set ranging mode to centimeters
    cm_mode = 0x51
    first_echo_low = 0x03
    first_echo_high = 0x02
    range_value = 140
    gain_value = 3
    value = 0.0
    debug = False

    def __init__(self, address, debug=False):
        self.debug = debug
        self.logger = logging.getLogger(
            'tiberius.control.UltrasonicRangefinder')
        self.logger.info(
            'Creating an instance of UltrasonicRangefinder (%s)', str(
                hex(address)))

        self.bus = smbus.SMBus(1)
        self.address = address
        try:
            self.bus.write_byte_data(
                self.address, self.rangereg, self.range_value)
            self.bus.write_byte_data(
                self.address, self.gainreg, self.gain_value)
        except IOError:
            if self.debug:
                self.logger.error('I2C write error %s', hex(self.address))

    def doranging(self):
        try:
            self.bus.write_byte_data(
                self.address, self.commandreg, self.cm_mode)
            return True
        except IOError:
            if self.debug:
                self.logger.error('I2C write error %s', hex(self.address))
            return False

    def getranging(self):
        try:
            high_byte = self.bus.read_byte_data(
                self.address, self.first_echo_high)
            low_byte = self.bus.read_byte_data(
                self.address, self.first_echo_low)
            if ((high_byte << 8) + low_byte) == 0:
                # If we failed to range say the data is not valid.
                return False
            else:
                value = (high_byte << 8) + low_byte
            return value

        except IOError:
            if self.debug:
                self.logger.error('IO error getranging %s', hex(self.address))
            # If we failed to range say the data is not valid.
            return False
