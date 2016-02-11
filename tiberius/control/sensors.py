#import rplidar
import cmps11
import srf08
import time
from tiberius.config.config_parser import TiberiusConfigParser
from tiberius.control.gps20 import GlobalPositioningSystem
#import picamera
#import gps


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
        self.srfrr.doranging()
        self.srffc.doranging()
        self.srffl.doranging()
        self.srfrr.doranging()
        self.srfrc.doranging()
        self.srfrl.doranging()

        # We need to wait for the measurement to be made before reading the
        # result.
        time.sleep(0.065)

        # Read the data from sensor's memory
        fr = self.srffr.getranging()
        fc = self.srffc.getranging()
        fl = self.srffl.getranging()
        rr = self.srfrr.getranging()
        rc = self.srfrc.getranging()
        rl = self.srfrl.getranging()

        return {'fl': fl, 'fc': fc, 'fr': fr, 'rl': rl, 'rc': rc, 'rr': rr}



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
        self.gps.update()
        gps_latitude = self.gps.latitude
        gps_longitude = self.gps.longitude
        gps_northsouth = self.gps.northsouth
        gps_eastwest = self.gps.eastwest
        gps_altitude = self.gps.altitude
        gps_variation = self.gps.variation
        gps_velocity = self.gps.velocity

        return {'latitude': gps_latitude, 'longitude': gps_longitude, 'northsouth': gps_northsouth, 'eastwest' : gps_eastwest,
                    'altitude' : gps_altitude, 'variation' : gps_variation, 'velocity' :gps_velocity}

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
