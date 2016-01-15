import ConfigParser

ULTRASONICS_SECTION = 'ultrasonics'

class TiberiusConfigParser():
	def __init__(self):
		self.parser = ConfigParser.ConfigParser()
		self.parser.read('/etc/tiberius/tiberius_conf.conf')
	@staticmethod
	def getParser():
		parser =  ConfigParser.ConfigParser()
		parser.read('/etc/tiberius/tiberius_conf.conf')
		return parser
	'''******************************************
		Constant values
	******************************************'''
	INSTALLED = 'installed'
	LIDAR_SECTION = 'lidar'
	MOTORS_SECTION = 'motors'
	COMPASS_SECTION = 'compass'
	STEERING_SECTION = 'steering'
	POWER_SECTION = 'power'
	NETWORKING_SECTION = 'networking'
	KINECT_SECTION = 'kinect'
	ROBOT_ARM_SECTION = 'arm'

	'''******************************************
		LIDAR
	******************************************'''
	@classmethod
	def isLidarEnabled():
		return TiberiusConfigParser.getParser().getboolean(self.LIDAR_SECTION, 'installed')

	'''******************************************
	        Motors
	******************************************'''
	@classmethod
	def getMotorFrontLeftAddress():
		addr = TiberiusConfigParser.getParser().get(self.MOTORS_SECTION, 'front_left')
		return int(addr)

	@classmethod
	def getMotorFrontRightAddress():
		addr = TiberiusConfigParser.getParser().get(self.MOTORS_SECTION, 'front_right')
		return int(addr)

	@classmethod
	def getMotorRearRightAddress():
                addr = TiberiusConfigParser.getParser().get(self.MOTORS_SECTION, 'rear_right')
                return int(addr)
	
	@classmethod
	def getMotorRearLeftAddress():
                addr = TiberiusConfigParser.getParser().get(self.MOTORS_SECTION, 'rear_left')
                return int(addr)

	'''******************************************
		Ultrasonics
	******************************************'''
	@classmethod
	def getUltrasonicFrontCentreAddress():
		addr = TiberiusConfigParser.getParser().get(self.ULTRASONICS_SECTION, 'front_centre')
		return int(addr)
	@classmethod

	def getUltrasonicFrontLeftAddress():
		addr = TiberiusConfigParser.getParser().get(self.ULTRASONICS_SECTION, 'front_left')
		return int(addr)

	@staticmethod
	def getUltrasonicFrontRightAddress():
		addr = TiberiusConfigParser.getParser().get(ULTRASONICS_SECTION, 'front_right')
		return int(addr)

	@classmethod
	def getUltrasonicRearCentreAddress():
		addr = TiberiusConfigParser.getParser().get(self.ULTRASONICS_SECTION, 'rear_centre')
		return int(addr)

	@classmethod
	def getUltrasonicRearLeftAddress():
		addr = TiberiusConfigParser.getParser().get(self.ULTRASONICS_SECTION, 'rear_left')
		return int(addr)

	@classmethod
	def getUltrasonicRearRightAddress():
		addr = TiberiusConfigParser.getParser().get(self.ULTRASONICS_SECTION, 'rear_right')
		return int(addr)

	'''******************************************
		Compass
	******************************************'''

	@classmethod
	def isCompassEnabled():
		return TiberiusConfigParser.getParser().getboolean(self.COMPASS_SECTION, 'installed')

	@classmethod		
	def getCompassAddress():
		addr = TiberiusConfigParser.getParser().get(self.COMPASS_SECTION, 'address')
		return int(addr)

	'''******************************************
		Networking
	******************************************'''

	@classmethod
	def getIPAddress():
		ipa = TiberiusConfigParser.getParser().get(self.NETWORKING_SECTION, 'ip_address')
		return ipa

	'''
	A setter method is required to deal with IP address changes if using DHCP.
	'''
	@classmethod
	def setIPAddress(self, ip_address):
		result = TiberiusConfigParser.getParser().set(self.NETWORKING_SECTION, 'ip_address', ip_address)
		return result

	@classmethod
	def getName():
		name = TiberiusConfigParser.getParser().get(self.NETWORKING_SECTION, 'name')
		return name

	'''******************************************
		Steering
	******************************************'''

	@classmethod
	def getSteeringType():
		type = TiberiusConfigParser.getParser().get(self.STEERING_SECTION, 'type')
		return type

	'''******************************************
		Power
	******************************************'''

	@classmethod
	def getBatteryCapacity():
		capacity = TiberiusConfigParser.getParser().get(self.POWER_SECTION, 'capacity')
		return capacity

	@classmethod
	def getBatteryChemistry():
		chemistry = TiberiusConfigParser.getParser().get(self.POWER_SECTION, 'chemistry')
		return chemistry

if __name__ == "__main__":
	c = TiberiusConfigParser()
	ip_address = c.getIPAddress()
	print ip_address
