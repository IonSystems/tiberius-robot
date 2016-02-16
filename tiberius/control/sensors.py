#!/usr/bin/env python
import cmps11
import srf08
import time
from tiberius.config.config_parser import TiberiusConfigParser
from tiberius.control.gps20 import GlobalPositioningSystem


class Ultrasonic:
    '''
        Contains the ultrasonic sensors, and methods to receive data from them.
        Data is returned from teh sensors in centimeters.
    '''

    # Front Right
    srffr = srf08.UltrasonicRangefinder(
        TiberiusConfigParser.getUltrasonicFrontRightAddress())
    # Front Centre
    srffc = srf08.UltrasonicRangefinder(
        TiberiusConfigParser.getUltrasonicFrontCentreAddress())
    # Front Left
    srffl = srf08.UltrasonicRangefinder(
        TiberiusConfigParser.getUltrasonicFrontLeftAddress())
    # Rear Right
    srfrr = srf08.UltrasonicRangefinder(
        TiberiusConfigParser.getUltrasonicRearRightAddress())
    # Rear Centre
    srfrc = srf08.UltrasonicRangefinder(
        TiberiusConfigParser.getUltrasonicRearCentreAddress())
    # Rear Left
    srfrl = srf08.UltrasonicRangefinder(
        TiberiusConfigParser.getUltrasonicRearLeftAddress())

    def senseUltrasonic(self):
        # Tell sensors to write data to it's memory

        # We need to check each sensor and make sure its giving us valid data.
        # So if we fail to write to a sensor we need to mark it as invalid.

        valid = []
        valid[0] = self.srfrr.doranging()
        valid[1] = self.srffc.doranging()
        valid[2] = self.srffl.doranging()
        valid[3] = self.srfrr.doranging()
        valid[4] = self.srfrc.doranging()
        valid[5] = self.srfrl.doranging()

        # We need to wait for the measurement to be made before reading the
        # result.
        time.sleep(0.065)

        # Read the data from sensor's memory

        data = []
        data[0] = self.srffr.getranging()
        data[1] = self.srffc.getranging()
        data[2] = self.srffl.getranging()
        data[3] = self.srfrr.getranging()
        data[4] = self.srfrc.getranging()
        data[5] = self.srfrl.getranging()

        # Check if the data is valid
        for i in range(0, 5):
            if data[i] is False:
                valid[i] = False
                data[i] = 0  # Best to assume we might crash rather than
                # risk it (0 means that any badly written scripts *should* stop)
                # Also by putting a 0 in the data we can still add the row to the database.

        return {'fr': data[0],
                'fc': data[1],
                'fl': data[2],
                'rr': data[3],
                'rc': data[4],
                'rr': data[5],
                'valid': valid}

    def frontHit(self, d=30):
        results = self.senseUltrasonic()

        return ((results['fl'] < d) or
                (results['fc'] < d) or
                (results['fr'] < d))

    def rearHit(self, d=30):
        results = self.senseUltrasonic()

        return ((results['rl'] < d) or
                (results['rc'] < d) or
                (results['rr'] < d))

    def anythingHit(self, d=30):
        results = self.senseUltrasonic()

        return ((results['rl'] < d) or
                (results['rc'] < d) or
                (results['rr'] < d) or
                (results['rl'] < d) or
                (results['rc'] < d) or
                (results['rr'] < d))

# class Lidar:
#	lidar = RoboPeakLidar()

    # TODO: This will eventually include methods such as generateImage(),
    # fetchData() or similar

# class TimeOfFlight:
    # If we ever get a TOF sensor.

# class Camera:
#	'''
#		Provides camera capture methods.
#	'''
#	camera = picamera.PiCamera()
#
#	def capture_image(self):
#		self.camera.resolution = (640,480)
#		self.camera.capture('./pi_camera_image.jpg')
if TiberiusConfigParser.isCompassEnabled():
    class Compass:
        '''
                Provides compass related methods, what more can I say?
        '''

        compass = cmps11.TiltCompensatedCompass(
            TiberiusConfigParser.getCompassAddress())

        def headingDegrees(self):
            # Get the heading in degrees.
            try:
                raw = int(self.compass.heading())
            except:
                return 222.2
            return raw / 10

        def getMostRecentDegrees(self):
            return self.compass.getMostRecentDegrees()

        def headingNormalized(self):
            angle = int(self.headingDegrees())
            while(angle > 180):
                angle -= 360
            while(angle < -180):
                angle += 360
            return angle


class GPS:
    def __init__(self):
        self.gps = GlobalPositioningSystem()

    def read_gps(self):
        return self.gps.read_gps()

    def has_fix(self):
        return self.gps.has_fix()


class I2CReadError(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class I2CWriteError(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
