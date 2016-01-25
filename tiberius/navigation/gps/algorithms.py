import math

from tiberius.control.gps20 import GlobalPositioningSystem
from tiberius.control.control import Control


class Algorithms:
	"""
		Set of algorithms that control tiberius using the gps and compass.


		Point to point algorithm moves from one longitude and latitude position
		to another. Created

		Follow path algorithm moves to a location using multiple point to point calls
		to create a path that can move around objects or along a given path. TODO
	"""
	def __init__(self):
		self.gps = GlobalPositioningSystem()
		self.control = Control()
		self.SPEED = 0.5  # meters/second

    # get the current location of tiberius
	def getLocation(self):
		return [self.gps.longitude, self.gps.latitude]

	def getHeading(self, curlocation, destination):
		curlongitude = float(curlocation[0])
		curlatitude = float(curlocation[1])
		deslongitude = float(destination[0])
		deslatitude = float(destination[1])

		y = math.sin(deslongitude - curlongitude) * math.cos(deslatitude)
		x = math.cos(curlatitude) * math.sin(deslatitude) - \
			math.sin(curlatitude) * math.cos(deslatitude) * math.cos(deslongitude - curlongitude)
		heading = math.degrees(math.atan2(y, x) + 360) % 360

		return heading

	def getDistance(self, curlocation, destination):
		r = 6371000  # radius of the earth in meters
		longdis = float(curlocation[0]) - float(destination[0])
		latdis = float(curlocation[1]) - float(destination[1])
		a = math.sin(latdis / 2) * math.sin(latdis / 2) + \
			math.cos(float(curlocation[1])) * math.cos(float(destination[1])) * \
			math.sin(longdis / 2) * math.sin(longdis / 2)
		c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
		distance = r * c
		return distance

# move from current location to a given destination (a longitude and latitude)
	def pointToPoint(self, destination, checkdistance=1, speedpercent=50):
		if self.gps.longitude == None:
			print 'NO FIX'
			return
		speed = 100 / speedpercent
		curlocation = self.getLocation()
		heading = self.getHeading(curlocation, destination)
		distance = self.getDistance(curlocation, destination)
		time = checkdistance / (self.SPEED / speed)
		self.control.turnTo(heading)
		while distance > checkdistance:
			self.control.driveStraight(speedpercent, time)
			distance -= checkdistance
			curlocation = self.getLocation()
			newheading = self.getHeading(curlocation, destination)
			if not (heading + 5 < newheading < 5 - heading):
				heading = newheading
				distance = self.getDistance(curlocation, destination)
				self.control.turnTo(heading)
		curlocation = self.getLocation()
		heading = self.getHeading(curlocation, destination)
		distance = self.getDistance(curlocation, destination)
		time = distance / (self.SPEED / speed)
		self.control.turnTo(heading)
		self.control.driveStraight(speedpercent, time)
		print "The task is complete"
		print "The current location of tiberius is : " + curlocation
		print "with the desired location being : " + destination
