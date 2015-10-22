#import rplidar
import cmps11
import srf08
#import picamera
#import gps

class Ultrasonic:
	'''
		Contains the ultrasonic sensors, and methods to receive data from them.
		Data is returned from teh sensors in centimeters.
	'''

	#Front Right
	srffr = srf08.UltrasonicRangefinder(0x72)
	#Front Centre
	srffc = srf08.UltrasonicRangefinder(0x71)
	#Front Left
	srffl = srf08.UltrasonicRangefinder(0x70)
	#Rear Right
	srfrr = srf08.UltrasonicRangefinder(0x73)
	#Rear Centre
	srfrc = srf08.UltrasonicRangefinder(0x74)
	#Rear Left
	srfrl = srf08.UltrasonicRangefinder(0x75)

	def senseUltrasonic(self):
		#Tell sensors to write data to it's memory
		# TODO: Currently the doranging() method does all sensors, a bit dodgy
		self.srfrr.doranging()

		# Read the data from sensor's memory
		fr = self.srffr.getranging()
		fc = self.srffc.getranging()
		fl = self.srffl.getranging()
		rr = self.srfrr.getranging()
		rc = self.srfrc.getranging()
		rl = self.srfrl.getranging()

		return {'fl':fl, 'fc':fc , 'fr':fr, 'rl':rl, 'rc':rc , 'rr':rr}

#class Lidar:
#	lidar = RoboPeakLidar()

	#TODO: This will eventually include methods such as generateImage(), fetchData() or similar

#class TimeOfFlight:
	#If we ever get a TOF sensor.

#class Camera:
#	'''
#		Provides camera capture methods.
#	'''
#	camera = picamera.PiCamera()
#
#	def capture_image(self):
#		self.camera.resolution = (640,480)
#		self.camera.capture('./pi_camera_image.jpg')

class Compass:
	'''
		Provides compass related methods, what more can I say?
	'''
	compass = cmps11.TiltCompensatedCompass()

	def headingDegrees(self):
		# Get the heading in degrees.
		raw = int(self.compass.heading())
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

#class GPS:
	#gps =
