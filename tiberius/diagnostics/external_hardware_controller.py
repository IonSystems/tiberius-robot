import serial
from tiberius.utils import detection
import time
import tiberius.database.query as db_q
from tiberius.database.tables import CompassTable

class ExternalHardwareController:
    if detection.detect_windows():
        port = 'COM8'
    else:
        port = '/dev/ttyACM3'
    baud = 115200

    diagnostic_led_data = [0, 0, 0, 0, 0, 0, 0, 0]
    ring_led_data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    relay_data = [0, 0, 0, 0]
    servo_data = [75]

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
            print "EHC DATA: " + str(data_message)
            self.ser.write(data_message)


def compass_monitor(control):

    dicti = db_q.get_latest(CompassTable)

    if dicti is not None:

        bearing = dicti[0].heading
        print "Bearing: " + str(bearing)
        if 7.5 > bearing > -7.5:
            control.ehc.set_hardware(None, [1, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9], None, None)
        elif -7.5 > bearing > -22.5:
            control.ehc.set_hardware(None, [9, 1, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9], None, None)
        elif -22.5 > bearing > -37.5:
            control.ehc.set_hardware(None, [9, 9, 1, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9], None, None)
        elif -37.5 > bearing > -52.5:
            control.ehc.set_hardware(None, [9, 9, 9, 1, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9], None, None)
        elif -52.5 > bearing > -67.5:
            control.ehc.set_hardware(None, [9, 9, 9, 9, 1, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9], None, None)
        elif -67.5 > bearing > -82.5:
            control.ehc.set_hardware(None, [9, 9, 9, 9, 9, 1, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9], None, None)
        elif -82.5 > bearing > -97.5:
            control.ehc.set_hardware(None, [9, 9, 9, 9, 9, 9, 1, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9], None, None)
        elif -97.5 > bearing > -112.5:
            control.ehc.set_hardware(None, [9, 9, 9, 9, 9, 9, 9, 1, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9], None, None)
        elif -112.5 > bearing > -127.5:
            control.ehc.set_hardware(None, [9, 9, 9, 9, 9, 9, 9, 9, 1, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9], None, None)
        elif -127.5 > bearing > -142.5:
            control.ehc.set_hardware(None, [9, 9, 9, 9, 9, 9, 9, 9, 9, 1, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9], None, None)
        elif -142.5 > bearing > -157.5:
            control.ehc.set_hardware(None, [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 1, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9], None, None)
        elif -157.5 > bearing > -172.5:
            control.ehc.set_hardware(None, [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 1, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9], None, None)
        elif 22.5 > bearing > 7.5:
            control.ehc.set_hardware(None, [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 1, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9], None, None)
        elif 37.5 > bearing > 22.5:
            control.ehc.set_hardware(None, [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 1, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9], None, None)
        elif 52.5 > bearing > 37.5:
            control.ehc.set_hardware(None, [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 1, 9, 9, 9, 9, 9, 9, 9, 9, 9], None, None)
        elif 67.5 > bearing > 52.5:
            control.ehc.set_hardware(None, [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 1, 9, 9, 9, 9, 9, 9, 9, 9], None, None)
        elif 82.5 > bearing > 67.5:
            control.ehc.set_hardware(None, [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 1, 9, 9, 9, 9, 9, 9, 9], None, None)
        elif 97.5 > bearing > 82.5:
            control.ehc.set_hardware(None, [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 1, 9, 9, 9, 9, 9, 9], None, None)
        elif 112.5 > bearing > 97.5:
            control.ehc.set_hardware(None, [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 1, 9, 9, 9, 9, 9], None, None)
        elif 127.5 > bearing > 112.5:
            control.ehc.set_hardware(None, [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 1, 9, 9, 9, 9], None, None)
        elif 142.5 > bearing > 127.5:
            control.ehc.set_hardware(None, [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 1, 9, 9, 9], None, None)
        elif 157.5 > bearing > 142.5:
            control.ehc.set_hardware(None, [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 1, 9, 9], None, None)
        elif 172.5 > bearing > 157.5:
            control.ehc.set_hardware(None, [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 1, 9], None, None)
        elif 172.5 < bearing < -172.5:
            control.ehc.set_hardware(None, [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 1], None, None)
    else:
        print "No Compass Data"
        control.ehc.set_hardware(None, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], None, None)


















