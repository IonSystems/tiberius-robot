import serial
from tiberius.utils import detection
import time


class diagnostics_leds:
    if detection.detect_windows():
        port = 'COM8'
    else:
        port = '/dev/ttyACM1'
    baud = 9600

    def __init__(self, debug=False):
        self.ser = serial.Serial(self.port, self.baud, timeout=1)
        try:
            self.ser.open()

        except:
            print "Port already open or in use"
        time.sleep(3)

    def setLEDs(self, led0=-1, led1=-1, led2=-1, led3=-1, led4=-1, led5=-1, led6=-1, led7=-1):
        if not self.ser.is_open:
            try:
                self.ser.open()
            except:
                print "Port already open or in use"
            time.sleep(3)
        if self.ser.is_open:
            data = "sd" + str(led0) + "d" + str(led1) + "d" + str(led2) + "d" + str(led3) + "d" + str(led4) + "d" + str(
                led5) + "d" + str(led6) + "d" + str(led7)

            self.ser.write(data)


if __name__ == "__main__":
    # from tiberius.diagnostics.diagnostics_leds import diagnostics_leds
    from random import randint

    leds = diagnostics_leds()

    l1, l2, l3, l4, l5, l6, l7, l8 = 0, 0, 0, 0, 0, 0, 0, 0

    while (True):
        leds.setLEDs(l1, l2, l3, l4, l5, l6, l7, l8)
        l1 = randint(0, 5)
        l2 = randint(0, 5)
        l3 = randint(0, 5)
        l4 = randint(0, 5)
        l5 = randint(0, 5)
        l6 = randint(0, 5)
        l7 = randint(0, 5)
        l8 = randint(0, 5)
        time.sleep(0.1)
