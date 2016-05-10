#!/usr/bin/python
import sys
from tiberius.utils import detection
# If i2c not available, use the dummy smbus library to allow
# simulation of I2C transactions.
if not detection.i2c_available():
    from tiberius.smbus_dummy import smbus
else:
    import smbus
from tiberius.logger import logger
import logging
from enum import Enum


class MotorDriver:
    '''
    An instance of this class is created for each motor.
    This driver interfaces with the motor using I2C.
    This driver interfaces with an MD03 Motor Driver.
    '''

    def __init__(self, address, debug=False, inverted=False):
        self.logger = logging.getLogger('tiberius.control.MotorDriver')
        self.logger.info('Creating an instance of MotorDriver')

        self.bus = smbus.SMBus(1)
        self.address = address
        self.debug = debug
        self.inverted = inverted

        self.direction_register = 0x00
        self.status_register = 0x01
        self.speed_register = 0x02
        self.accel_register = 0x03
        self.temp_register = 0x04
        self.current_register = 0x05
        self.version_register = 0x07

        self.version = self.version()

    class Direction(Enum):
        NONE = 0
        FORWARD = 1
        BACKWARD = 2

    def direction(self):
        # 1 = forwards, 2 = reverse
        direction = self.bus.read_byte_data(
            self.address, self.direction_register)
        return direction

    def temperature(self):
        temp = self.bus.read_byte_data(self.address, self.temp_register)
        # TODO work out degrees
        return temp

    '''Gets the current speed of the motor (0 to 255)'''

    def speed(self):
        speed = self.bus.read_byte_data(self.address, self.speed_register)
        return speed

    '''Gets the current acceleration of the motor (0 to 255)'''

    def acceleration(self):
        accel = self.bus.read_byte_data(self.address, self.accel_register)
        return accel

    '''Returns a current value between 0(0A) and 186(20A)'''

    def current(self):
        current = self.bus.read_byte_data(self.address, self.current_register)
        amps = round(((current / 186.0) * 20.0), 3)
        return amps

    def version(self):
        version = self.bus.read_byte_data(self.address, self.version_register)
        return version

    '''    Returns the status register bits:
        0: Acceleration in progress LSB
        1: Over-current indicator
        2: Over-temperature indicator
        The bits are returned in dictionary form.
    '''

    def status(self):
        status = self.bus.read_byte_data(self.address, self.status_register)
        return status

    def register_dump(self):
        dict = {'speed': 0, 'acceleration': 0, 'direction': 0}
        dict['speed'] = self.speed()
        dict['acceleration'] = self.acceleration()
        dict['direction'] = self.direction()
        return dict

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

    '''
        NOTE: Ensure rear facing motors are wired opposite from the rest.
    '''

    def move(self, speed, accel):
        try:
            # Set acceleration, must be done before direction register.
            self.bus.write_byte_data(self.address, self.accel_register, accel)
            speed = int(speed)
            if speed == 0:
                # Make sure to set speed and acceleration before issuing direction
                # to ensure the motors don't start turning in the wrong
                # direction
                self.bus.write_byte_data(
                    self.address, self.speed_register, speed)
                self.bus.write_byte_data(
                    self.address,
                    self.direction_register,
                    self.Direction.NONE.value)

            # If we want to go forward, set direction reg to 1
            elif (speed > 0):
                # Make sure to set speed and acceleration before issuing direction
                # to ensure the motors don't start turning in the wrong
                # direction
                self.bus.write_byte_data(
                    self.address, self.speed_register, speed)
                self.bus.write_byte_data(
                    self.address,
                    self.direction_register,
                    self.Direction.FORWARD.value)

            # If we want to go backward, set direction register to 2
            elif (speed < 0):
                # Make sure to set speed and acceleration before issuing direction
                # to ensure the motors don't start turning in the wrong
                # direction
                self.bus.write_byte_data(
                    self.address, self.speed_register, -speed)
                self.bus.write_byte_data(
                    self.address,
                    self.direction_register,
                    self.Direction.BACKWARD.value)

        except IOError as e:
            self.logger.warn(
                'IO error on I2C bus, address %s (%s)', hex(
                    self.address), e)
