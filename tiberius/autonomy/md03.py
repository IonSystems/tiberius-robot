#!/usr/bin/python

import smbus


class md03:

    def __init__(self, address, debug=False):
        self.bus = smbus.SMBus(1)
        self.address = address
        self.debug = debug

    def move(self, speed, accel):
        try:
            if ((speed < -255) or (speed > 255)):
                print 'Speed parameter out of range.'
                return 0

            if ((accel < 0) or (accel > 255)):
                print 'Acceleration parameter out of range.'
                return 0

            self.bus.write_byte_data(self.address, 3, accel)
            if (speed >= 0):
                if (self.debug):
                    print speed
                self.bus.write_byte_data(self.address, 2, int(speed))
                # the way the motors are installed on the robot
                # 0x59 and 0x5B go forward when receive reverse command
                if ((self.address == 0x58) or (self.address == 0x5A)):
                    self.bus.write_byte_data(self.address, 0, 1)
                if ((self.address == 0x59) or (self.address == 0x5B)):
                    self.bus.write_byte_data(self.address, 0, 2)
            if (speed < 0):
                if (self.debug):
                    print speed
                self.bus.write_byte_data(self.address, 2, int(-speed))
                if ((self.address == 0x58) or (self.address == 0x5A)):
                    self.bus.write_byte_data(self.address, 0, 2)
                if ((self.address == 0x59) or (self.address == 0x5B)):
                    self.bus.write_byte_data(self.address, 0, 1)
            return 1

        except IOError:
            print 'IO error move', hex(self.address)
