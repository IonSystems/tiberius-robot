import math
import null as null

from tiberius.control.gps20 import GlobalPositioningSystem

class Algorithms:
	'''
		Set of algorithms that control tiberius using the gps and compass


	'''

	def __init__(self):
		self.gps = GlobalPositioningSystem()

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

	# move from current location to a given destination (a longitude and latitude)
	def pointToPoint(self, destination):

		curlocation = self.getLocation()
		heading = self.getHeading(curlocation, destination)
		

		return null
