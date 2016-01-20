import platform
import re
import os

'''
    This detction method is based on the Adafruit GPIO library,
    that can be found here:
    https://github.com/adafruit/Adafruit_Python_GPIO/blob/master/Adafruit_GPIO/Platform.py
'''
def detect_pi():
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

def detect_windows():
    return 'nt' in os.name

if __name__ == "__main__":
    print 'Raspberry Pi detected?: ' + detect_pi()
    print 'Windows detected?: ' + detect_windows()
