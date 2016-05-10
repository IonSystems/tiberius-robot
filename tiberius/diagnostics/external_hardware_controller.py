import serial
from tiberius.utils import detection
import time


class ExternalHardwareController:
    if detection.detect_windows():
        port = 'COM8'
    else:
        port = '/dev/ttyACM0'
    baud = 115200

    diagnostic_led_data = {0, 0, 0, 0, 0, 0, 0, 0}
    ring_led_data = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0}
    relay_data = {0, 0, 0, 0}
    servo_data = {75}

    def __init__(self, debug=False):
        self.ser = serial.Serial(self.port, self.baud, timeout=1)

    def set_hardware(self, diagnostics_leds=None, ring_leds=None, relays=None, servos=None):
        if not self.ser.isOpen():
            try:
                self.ser.open()
            except:
                print "Port already open"
            time.sleep(10)
        if self.ser.isOpen():
            if diagnostics_leds is not None:
                self.diagnostic_led_data = diagnostics_leds
            if ring_leds is not None:
                self.ring_led_data = ring_leds
            if relays is not None:
                self.relay_data = relays
            if servos is not None:
                self.servo_data = servos

            data_message = "s"
            for data in self.diagnostic_led_data:
                data_message += "d" + str(data)

            for data in self.ring_led_data:
                data_message += "d" + str(data)

            for data in self.relay_data:
                data_message += "d" + str(data)

            for data in self.servo_data:
                data_message += "d" + str(data)

            self.ser.write(data_message)


if __name__ == "__main__":
    from random import randint

    externalHardwareController = ExternalHardwareController()

    l1, l2, l3, l4, l5, l6, l7, l8 = 0, 0, 0, 0, 0, 0, 0, 0

    while (True):
        externalHardwareController.set_hardware({l1, l2, l3, l4, l5, l6, l7, l8})
        l1 = randint(0, 5)
        l2 = randint(0, 5)
        l3 = randint(0, 5)
        l4 = randint(0, 5)
        l5 = randint(0, 5)
        l6 = randint(0, 5)
        l7 = randint(0, 5)
        l8 = randint(0, 5)
        time.sleep(0.1)


def compass_monitor(bearing):
    if 7.5 > bearing > -7.5:
        externalHardwareController.set_hardware(None, {1, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9}, None, None)
    elif -7.5 > bearing > -22.5:
        externalHardwareController.set_hardware(None, {9, 1, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9}, None, None)
    elif -22.5 > bearing > -37.5:
        externalHardwareController.set_hardware(None, {9, 9, 1, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9}, None, None)
    elif -37.5 > bearing > -52.5:
        externalHardwareController.set_hardware(None, {9, 9, 9, 1, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9}, None, None)
    elif -52.5 > bearing > -67.5:
        externalHardwareController.set_hardware(None, {9, 9, 9, 9, 1, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9}, None, None)
    elif -67.5 > bearing > -82.5:
        externalHardwareController.set_hardware(None, {9, 9, 9, 9, 9, 1, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9}, None, None)
    elif -82.5 > bearing > -97.5:
        externalHardwareController.set_hardware(None, {9, 9, 9, 9, 9, 9, 1, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9}, None, None)
    elif -97.5 > bearing > -112.5:
        externalHardwareController.set_hardware(None, {9, 9, 9, 9, 9, 9, 9, 1, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9}, None, None)
    elif -112.5 > bearing > -127.5:
        externalHardwareController.set_hardware(None, {9, 9, 9, 9, 9, 9, 9, 9, 1, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9}, None, None)
    elif -127.5 > bearing > -142.5:
        externalHardwareController.set_hardware(None, {9, 9, 9, 9, 9, 9, 9, 9, 9, 1, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9}, None, None)
    elif -142.5 > bearing > -157.5:
        externalHardwareController.set_hardware(None, {9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 1, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9}, None, None)
    elif -157.5 > bearing > -172.5:
        externalHardwareController.set_hardware(None, {9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 1, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9}, None, None)
    elif 22.5 > bearing > 7.5:
        externalHardwareController.set_hardware(None, {9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 1, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9}, None, None)
    elif 37.5 > bearing > 22.5:
        externalHardwareController.set_hardware(None, {9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 1, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9}, None, None)
    elif 52.5 > bearing > 37.5:
        externalHardwareController.set_hardware(None, {9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 1, 9, 9, 9, 9, 9, 9, 9, 9, 9}, None, None)
    elif 67.5 > bearing > 52.5:
        externalHardwareController.set_hardware(None, {9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 1, 9, 9, 9, 9, 9, 9, 9, 9}, None, None)
    elif 82.5 > bearing > 67.5:
        externalHardwareController.set_hardware(None, {9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 1, 9, 9, 9, 9, 9, 9, 9}, None, None)
    elif 97.5 > bearing > 82.5:
        externalHardwareController.set_hardware(None, {9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 1, 9, 9, 9, 9, 9, 9}, None, None)
    elif 112.5 > bearing > 97.5:
        externalHardwareController.set_hardware(None, {9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 1, 9, 9, 9, 9, 9}, None, None)
    elif 127.5 > bearing > 112.5:
        externalHardwareController.set_hardware(None, {9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 1, 9, 9, 9, 9}, None, None)
    elif 142.5 > bearing > 127.5:
        externalHardwareController.set_hardware(None, {9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 1, 9, 9, 9}, None, None)
    elif 157.5 > bearing > 142.5:
        externalHardwareController.set_hardware(None, {9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 1, 9, 9}, None, None)
    elif 172.5 > bearing > 157.5:
        externalHardwareController.set_hardware(None, {9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 1, 9}, None, None)
    elif 172.5 < bearing < -172.5:
        externalHardwareController.set_hardware(None, {9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 1}, None, None)
    else:
        externalHardwareController.set_hardware(None, {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0}, None, None)


















