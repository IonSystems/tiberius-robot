#!/usr/bin/python
import sys
from tiberius.utils import detection
# If not running on a raspberry pi, use the dummy smbus library to allow
# simulation of I2C transactions.
if not detection.detect_pi():
    from tiberius.smbus_dummy import smbus
else:
    import smbus


class TiltCompensatedCompass:

    def __init__(self, address):
        self.bus = smbus.SMBus(1)
        self.address = address

    # Used for future work on 'smart' readings
    # TODO:Will return previous reading rather
    # than reading a new reading that is probably the same.
    __heading = -1
    __heading_degrees = -1

    __pitch_filtered = -1
    __roll_filterd = -1

    __magnet_x = -1
    __magnet_y = -1
    __magnet_z = -1

    __accel_x = -1
    __accel_y = -1
    __accel_z = -1

    __gyro_x = -1
    __gyro_y = -1
    __gyro_z = -1

    __temp = -1

    __pitch_raw = -1
    __roll_raw = -1

    # Define register addresses
    COMPASS_8_BIT = 1
    COMPASS_H = 2
    COMPASS_L = 3

    PITCH_FILTERED = 4
    ROLL_FILTERED = 5

    MAGNET_X_H = 6
    MAGNET_X_L = 7
    MAGNET_Y_H = 8
    MAGNET_Y_L = 9
    MAGNET_Z_H = 10
    MAGNET_Z_L = 11

    ACCEL_X_H = 12
    ACCEL_X_L = 13
    ACCEL_Y_H = 14
    ACCEL_Y_L = 15
    ACCEL_Z_H = 16
    ACCEL_Z_L = 17

    GYRO_X_H = 18
    GYRO_X_L = 19
    GYRO_Y_H = 20
    GYRO_Y_L = 21
    GYRO_Z_H = 22
    GYRO_Z_L = 23

    TEMP_H = 24
    TEMP_L = 25

    PITCH_RAW = 26
    ROLL_RAW = 27

    '''******************************************
        Compass functions
    ******************************************'''

    def __read_compass_8(self):
        byte = self.bus.read_byte_data(self.address, self.COMPASS_8_BIT)
        self.__heading = byte
        return self.__heading

    def __read_compass_16(self):
        # cmps11 returns two 8 bit registers values
        # providing the range of 0-3599, representing 0 - 359.9 degrees
        high_byte = self.bus.read_byte_data(self.address, self.COMPASS_H)
        low_byte = self.bus.read_byte_data(self.address, self.COMPASS_L)
        self.__heading = float((high_byte << 8) + low_byte)
        return self.__heading

    '''******************************************
        Kalman filtered Pitch and Roll functions
    ******************************************'''

    def __read_filtered_pitch(self):
        byte = self.bus.read_byte_data(self.address, self.PITCH_FILTERED)
        self.__pitch_filtered = byte
        return self.__pitch_filtered

    def __read_filtered_roll(self):
        byte = self.bus.read_byte_data(self.address, self.ROLL_FILTERED)
        self.__roll_filtered = byte
        return self.__roll_filtered

    '''******************************************
        Magnetometer functions
    ******************************************'''

    def __read_magnetometer_x(self):
        high_byte = self.bus.read_byte_data(self.address, self.MAGNET_X_H)
        low_byte = self.bus.read_byte_data(self.address, self.MAGNET_X_L)
        self.__magnet_x = float((high_byte << 8) + low_byte)
        return self.__magnet_x

    def __read_magnetometer_y(self):
        high_byte = self.bus.read_byte_data(self.address, self.MAGNET_Y_H)
        low_byte = self.bus.read_byte_data(self.address, self.MAGNET_Y_L)
        self.__magnet_y = float((high_byte << 8) + low_byte)
        return self.__magnet_y

    def __read_magnetometer_z(self):
        high_byte = self.bus.read_byte_data(self.address, self.MAGNET_Z_H)
        low_byte = self.bus.read_byte_data(self.address, self.MAGNET_Z_L)
        self.__magnet_z = float((high_byte << 8) + low_byte)
        return self.__magnet_z

    '''******************************************
        Accelerometer functions
    ******************************************'''

    def __read_accelerometer_x(self):
        high_byte = self.bus.read_byte_data(self.address, self.ACCEL_X_H)
        low_byte = self.bus.read_byte_data(self.address, self.ACCEL_X_L)
        self.__accel_x = float((high_byte << 8) + low_byte)
        return self.__accel_x

    def __read_accelerometer_y(self):
        high_byte = self.bus.read_byte_data(self.address, self.ACCEL_Y_H)
        low_byte = self.bus.read_byte_data(self.address, self.ACCEL_Y_L)
        self.__accel_y = float((high_byte << 8) + low_byte)
        return self.__accel_y

    def __read_accelerometer_z(self):
        high_byte = self.bus.read_byte_data(self.address, self.ACCEL_Z_H)
        low_byte = self.bus.read_byte_data(self.address, self.ACCEL_Z_L)
        self.__accel_z = float((high_byte << 8) + low_byte)
        return self.__accel_z

    '''******************************************
        Gyroscope functions
    ******************************************'''

    def __read_gyroscope_x(self):
        high_byte = self.bus.read_byte_data(self.address, self.GYRO_X_H)
        low_byte = self.bus.read_byte_data(self.address, self.GYRO_X_L)
        self.__gyro_x = float((high_byte << 8) + low_byte)
        return self.__gyro_x

    def __read_gyroscope_y(self):
        high_byte = self.bus.read_byte_data(self.address, self.GYRO_Y_H)
        low_byte = self.bus.read_byte_data(self.address, self.GYRO_Y_L)
        self.__gyro_y = float((high_byte << 8) + low_byte)
        return self.__gyro_y

    def __read_gyroscope_z(self):
        high_byte = self.bus.read_byte_data(self.address, self.GYRO_Z_H)
        low_byte = self.bus.read_byte_data(self.address, self.GYRO_Z_L)
        self.__gyro_z = float((high_byte << 8) + low_byte)
        return self.__gyro_z

    '''******************************************
        Temperature function
    ******************************************'''

    def __read_temperature(self):
        high_byte = self.bus.read_byte_data(self.address, self.TEMP_H)
        low_byte = self.bus.read_byte_data(self.address, self.TEMP_H)
        self.__temp = float((high_byte << 8) + low_byte)
        return self.__temp

    '''******************************************
        Raw Pitch and Roll functions
    ******************************************'''

    def __read_raw_pitch(self):
        byte = self.bus.read_byte_data(self.address, self.PITCH_RAW)
        self.__pitch_raw = byte
        return self.__pitch_raw

    def __read_raw_roll(self):
        byte = self.bus.read_byte_data(self.address, self.ROLL_RAW)
        self.__roll_raw = byte
        return self.__roll_raw

    '''******************************************
        Accessible functions
    ******************************************'''

    def getMostRecentDegrees(self):
        # if self.__heading_degrees < 0:
        #    return False
        return self.__heading_degrees

    # TODO: We cannot rely on such a crude method for getting a heading
    def heading(self):
        '''
                Get the heading value between 0 and 3599.
        '''
        try:
            heading = self.__read_compass_16()
            return heading
        except IOError:
            raise self.CompassReadError("Error reading compass")

    def magnetometer(self):
        try:
            return [
                self.__read_magnetometer_x(),
                self.__read_magnetometer_y(),
                self.__read_magnetometer_z()]
        except IOError:
            raise self.CompassReadError("Error reading magnetometer.")

    def accelerometer(self):
        return [
            self.__read_accelerometer_x(),
            self.__read_accelerometer_y(),
            self.__read_accelerometer_z()]

    def gyroscope(self):
        return [
            self.__read_gyroscope_x(),
            self.__read_gyroscope_y(),
            self.__read_gyroscope_z()]

    def temperature(self):
        return self.__read_temperature()

    def pitch(self):
        return self.__read_filtered_pitch()

    def roll(self):
        return self.__read_filtered_roll()

# Test function
if __name__ == "__main__":
    cmps11 = TiltCompensatedCompass(66)
