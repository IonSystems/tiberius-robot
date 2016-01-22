import math
import null as null

from tiberius.control.gps20 import GlobalPositioningSystem
from tiberius.control.control import Control

class Algorithms:
	'''
		Set of algorithms that control tiberius using the gps and compass


	'''



	def __init__(self):
		self.gps = GlobalPositioningSystem()
		self.control = Control()
		self.SPEED = 0.5  # meters/second

	# get the current location of tiberius
	def getLocation(self):

		location = []
		location[0] = self.gps.longitude
		location[1] = self.gps.latitude

		return location

	def getHeading(self, curlocation, destination):
		curlongitude = curlocation[0]
		curlatitude = curlocation[1]
		deslongitude = destination[0]
		deslatitude = destination[1]

		y = math.sin(deslongitude - curlongitude) * math.cos(deslatitude)
		x = math.cos(curlatitude) * math.sin(deslatitude) - \
			math.sin(curlatitude) * math.cos(deslatitude) * math.cos(deslongitude - curlongitude)
		heading = math.degrees(math.atan2(y, x) + 360) % 360

		return heading

	def getDistance(self, curlocation, destination):
		r = 6371000  # radius of the earth in meters
		longdis = curlocation[0] - destination[0]
		latdis = curlocation[1] - destination[1]
		a = math.sin(latdis / 2) * math.sin(latdis / 2) + \
			math.cos(curlocation[1]) * math.cos(destination[1]) * \
			math.sin(longdis / 2) * math.sin(longdis / 2)
		c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
		distance = r * c
		return distance

	# move from current location to a given destination (a longitude and latitude)
	def pointToPoint(self, destination):

		curlocation = self.getLocation()
		heading = self.getHeading(curlocation, destination)
		distence = self.getDistance(curlocation, destination)
		time = distence / (self.SPEED / 2)
		self.control.turnTo(heading)
		self.control.driveStraight(50, time)
		print "The task is complete"
