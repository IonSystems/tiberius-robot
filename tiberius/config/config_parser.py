import ConfigParser

class TiberiusConfigParser():
	def __init__(self):
		self.parser = ConfigParser.ConfigParser()
		self.parser.read('/etc/tiberius/tiberius_conf.conf')

	'''******************************************
		Constant values
	******************************************'''
	INSTALLED = 'installed'
	LIDAR_SECTION = 'lidar'
	ULTRASONICS_SECTION = 'ultrasonics'
	COMPASS_SECTION = 'compass'
	STEERING_SECTION = 'steering'
	POWER_SECTION = 'power'
	NETWORKING_SECTION = 'networking'
	KINECT_SECTION = 'kinect'
	ROBOT_ARM_SECTION = 'arm'

	'''******************************************
		LIDAR
	******************************************'''
	def isLidarEnabled(self):
		return self.parser.getboolean(self.LIDAR_SECTION, 'installed')

	'''******************************************
		Ultrasonics
	******************************************'''

	def getUltrasonicFrontCentreAddress(self):
		addr = self.parser.get(self.ULTRASONICS_SECTION, 'front_centre')
		return int(addr)

	def getUltrasonicFrontLeftAddress(self):
		addr = self.parser.get(self.ULTRASONICS_SECTION, 'front_left')
		return int(addr)

	def getUltrasonicFrontRightAddress(self):
		addr = self.parser.get(self.ULTRASONICS_SECTION, 'front_right')
		return int(addr)

	def getUltrasonicRearCentreAddress(self):
		addr = self.parser.get(self.ULTRASONICS_SECTION, 'rear_centre')
		return int(addr)

	def getUltrasonicRearLeftAddress(self):
		addr = self.parser.get(self.ULTRASONICS_SECTION, 'rear_left')
		return int(addr)

	def getUltrasonicRearRightAddress(self):
		addr = self.parser.get(self.ULTRASONICS_SECTION, 'rear_right')
		return int(addr)

	'''******************************************
		Compass
	******************************************'''

	def getCompassAddress(self):
		addr = self.parser.get(self.COMPASS_SECTION, 'address')
		return int(addr)

	'''******************************************
		Networking
	******************************************'''
	def getIPAddress(self):
		ipa = self.parser.get(self.NETWORKING_SECTION, 'ip_address')
		return ipa

	'''
	A setter method is required to deal with IP address changes if using DHCP.
	'''
	def setIPAddress(self, ip_address):
		result = self.parser.set(self.NETWORKING_SECTION, 'ip_address', ip_address)
		return result

	def getName(self):
		name = self.parser.get(self.NETWORKING_SECTION, 'name')
		return name

	'''******************************************
		Steering
	******************************************'''

	def getSteeringType(self):
		type = self.parser.get(self.STEERING_SECTION, 'type')
		return type

	'''******************************************
		Power
	******************************************'''

	def getBatteryCapacity(self):
		capacity = self.parser.get(self.POWER_SECTION, 'capacity')
		return capacity

	def getBatteryChemistry(self):
		chemistry = self.parser.get(self.POWER_SECTION, 'chemistry')
		return chemistry

if __name__ == "__main__":
	c = TiberiusConfigParser()
	ip_address = c.getIPAddress()
	print ip_address
