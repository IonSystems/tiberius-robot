import platform
import re
import os

'''
    This detection method is based on the Adafruit GPIO library,
    that can be found here:
    https://github.com/adafruit/Adafruit_Python_GPIO/blob/master/Adafruit_GPIO/Platform.py
'''


def detect_pi():
    try:
        with open('/proc/cpuinfo', 'r') as infile:
            cpuinfo = infile.read()
        # Match a line like 'Hardware   : BCM2709'
        match = re.search('^Hardware\s+:\s+(\w+)$', cpuinfo,
                          flags=re.MULTILINE | re.IGNORECASE)
        if not match:
            # Couldn't find the hardware, assume it isn't a pi.
            return None
        if match.group(1) == 'BCM2708':
            # Pi 1
            return 1
        elif match.group(1) == 'BCM2709':
            # Pi 2
            return 2
        else:
            # Something else, not a pi.
            return None
    except IOError:
        return None
        print "Not a Pi"

def detect_windows():
    return 'nt' in os.name


def i2c_available():
    import smbus
    try:
        i2c = smbus.SMBus(1)
    except:
        return False
    return True

def detect_file(filename):
    return os.path.isfile(filename)

if __name__ == "__main__":
    print 'Raspberry Pi detected?: ' + str(detect_pi())
    print 'Windows detected?:      ' + str(detect_windows())
    print 'I2C available?:         ' + str(i2c_available())
