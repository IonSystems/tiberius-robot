import serial
from tiberius.utils import detection
import time

class ExternalHardwareController:
    if detection.detect_windows():
        port = 'COM8'
    else:
        port = '/dev/ttyACM3'
    baud = 115200

    diagnostic_led_data = [0, 0, 0, 0, 0, 0, 0, 0]
    ring_led_data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    relay_data = [1, 1, 1, 1]
    servo_data = [75]

    def __init__(self):
        self.ser = serial.Serial(self.port, self.baud, timeout=1)
        self.set_hardware()

    def set_hardware(self, diagnostics_leds=None, ring_leds=None, relays=None, servos=None):
        if not self.ser.isOpen():
            try:
                print "opening serial port"
                self.ser.open()
            except:
                print "Port already open"
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
            print "DLEDS: " + str(self.diagnostic_led_data)
            for data in self.diagnostic_led_data:
                data_message += "d" + str(data)

            print "ring: " + str(self.ring_led_data)
            for data in self.ring_led_data:
                data_message += "d" + str(data)

            print "relay: " + str(self.relay_data)
            for data in self.relay_data:
                data_message += "d" + str(data)

            print "servo: " + str(self.servo_data)
            for data in self.servo_data:
                data_message += "d" + str(data)
            data_message += "\n"
            print "EHC DATA: " + str(data_message)
            self.ser.write(data_message)


if __name__ == "__main__":
    from random import randint

    externalHardwareController = ExternalHardwareController()

    l1, l2, l3, l4, l5, l6, l7, l8 = 0, 0, 0, 0, 0, 0, 0, 0

    while (True):
        externalHardwareController.set_hardware([l1, l2, l3, l4, l5, l6, l7, l8])
        l1 = randint(0, 5)
        l2 = randint(0, 5)
        l3 = randint(0, 5)
        l4 = randint(0, 5)
        l5 = randint(0, 5)
        l6 = randint(0, 5)
        l7 = randint(0, 5)
        l8 = randint(0, 5)
        time.sleep(1)


def compass_monitor(poly):
    import tiberius.database.query as db_q
    from tiberius.database.tables import CompassTable

    dicti = db_q.get_latest(poly, CompassTable)

    if dicti is not None:

        bearing = dicti[0].heading
        print "Bearing: " + str(bearing)
        if 7.5 > bearing > -7.5:
            return [1, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9]
        elif -7.5 > bearing > -22.5:
            return [9, 1, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9]
        elif -22.5 > bearing > -37.5:
            return [9, 9, 1, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9]
        elif -37.5 > bearing > -52.5:
            return [9, 9, 9, 1, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9]
        elif -52.5 > bearing > -67.5:
            return [9, 9, 9, 9, 1, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9]
        elif -67.5 > bearing > -82.5:
            return [9, 9, 9, 9, 9, 1, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9]
        elif -82.5 > bearing > -97.5:
            return [9, 9, 9, 9, 9, 9, 1, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9]
        elif -97.5 > bearing > -112.5:
            return [9, 9, 9, 9, 9, 9, 9, 1, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9]
        elif -112.5 > bearing > -127.5:
            return [9, 9, 9, 9, 9, 9, 9, 9, 1, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9]
        elif -127.5 > bearing > -142.5:
            return [9, 9, 9, 9, 9, 9, 9, 9, 9, 1, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9]
        elif -142.5 > bearing > -157.5:
            return [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 1, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9]
        elif -157.5 > bearing > -172.5:
            return [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 1, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9]
        elif 22.5 > bearing > 7.5:
            return [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 1, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9]
        elif 37.5 > bearing > 22.5:
            return [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 1, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9]
        elif 52.5 > bearing > 37.5:
            return [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 1, 9, 9, 9, 9, 9, 9, 9, 9, 9]
        elif 67.5 > bearing > 52.5:
            return [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 1, 9, 9, 9, 9, 9, 9, 9, 9]
        elif 82.5 > bearing > 67.5:
            return [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 1, 9, 9, 9, 9, 9, 9, 9]
        elif 97.5 > bearing > 82.5:
            return [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 1, 9, 9, 9, 9, 9, 9]
        elif 112.5 > bearing > 97.5:
            return [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 1, 9, 9, 9, 9, 9]
        elif 127.5 > bearing > 112.5:
            return [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 1, 9, 9, 9, 9]
        elif 142.5 > bearing > 127.5:
            return [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 1, 9, 9, 9]
        elif 157.5 > bearing > 142.5:
            return [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 1, 9, 9]
        elif 172.5 > bearing > 157.5:
            return [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 1, 9]
        elif 172.5 < bearing < -172.5:
            return [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 1]
    else:
        print "No Compass Data"
        return [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


















