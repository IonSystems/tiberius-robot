import ConfigParser
from tiberius.utils import detection

'''******************************************
    Constant values
******************************************'''
ULTRASONICS_SECTION = 'ultrasonics'
INSTALLED = 'installed'
LIDAR_SECTION = 'lidar'
MOTORS_SECTION = 'motors'
COMPASS_SECTION = 'compass'
STEERING_SECTION = 'steering'
POWER_SECTION = 'power'
NETWORKING_SECTION = 'networking'
KINECT_SECTION = 'kinect'
ROBOT_ARM_SECTION = 'arm'
AUTHENTICATION_SECTION = 'authentication'


class TiberiusConfigParser():

    @staticmethod
    def getParser():
        parser = ConfigParser.ConfigParser()
        if detection.detect_windows():
            parser.read('D:\\tiberius\\tiberius_conf.conf')
        elif detection.detect_file('/etc/tiberius/tiberius_conf.conf'):
            parser.read('/etc/tiberius/tiberius_conf.conf')
        else:
            # Fall back to generic config file.
            parser.read('./tiberius_conf.conf')
        return parser

    '''******************************************
        LIDAR
    ******************************************'''
    @staticmethod
    def isLidarEnabled():
        return TiberiusConfigParser.getParser().getboolean(LIDAR_SECTION, 'installed')

    '''******************************************
        Motors
    ******************************************'''
    @staticmethod
    def getMotorFrontLeftAddress():
        addr = TiberiusConfigParser.getParser().get(MOTORS_SECTION, 'front_left')
        return int(addr)

    @staticmethod
    def getMotorFrontRightAddress():
        addr = TiberiusConfigParser.getParser().get(MOTORS_SECTION, 'front_right')
        return int(addr)

    @staticmethod
    def getMotorRearRightAddress():
        addr = TiberiusConfigParser.getParser().get(MOTORS_SECTION, 'rear_right')
        return int(addr)

    @staticmethod
    def getMotorRearLeftAddress():
        addr = TiberiusConfigParser.getParser().get(MOTORS_SECTION, 'rear_left')
        return int(addr)

    '''******************************************
        Ultrasonics
    ******************************************'''
    @staticmethod
    def getUltrasonicFrontCentreAddress():
        addr = TiberiusConfigParser.getParser().get(ULTRASONICS_SECTION, 'front_centre')
        return int(addr)

    @staticmethod
    def getUltrasonicFrontLeftAddress():
        addr = TiberiusConfigParser.getParser().get(ULTRASONICS_SECTION, 'front_left')
        return int(addr)

    @staticmethod
    def getUltrasonicFrontRightAddress():
        addr = TiberiusConfigParser.getParser().get(ULTRASONICS_SECTION, 'front_right')
        return int(addr)

    @staticmethod
    def getUltrasonicRearCentreAddress():
        addr = TiberiusConfigParser.getParser().get(ULTRASONICS_SECTION, 'rear_centre')
        return int(addr)

    @staticmethod
    def getUltrasonicRearLeftAddress():
        addr = TiberiusConfigParser.getParser().get(ULTRASONICS_SECTION, 'rear_left')
        return int(addr)

    @staticmethod
    def getUltrasonicRearRightAddress():
        addr = TiberiusConfigParser.getParser().get(ULTRASONICS_SECTION, 'rear_right')
        return int(addr)

    @staticmethod
    def areUltrasonicsEnabled():
        return TiberiusConfigParser.getParser().getboolean(ULTRASONICS_SECTION, 'installed')

    '''******************************************
        Compass
    ******************************************'''

    @staticmethod
    def isCompassEnabled():
        return TiberiusConfigParser.getParser().getboolean(COMPASS_SECTION, 'installed')

    @staticmethod
    def getCompassAddress():
        addr = TiberiusConfigParser.getParser().get(COMPASS_SECTION, 'address')
        return int(addr)


    '''******************************************
        Arm
    ******************************************'''

    @staticmethod
    def isArmEnabled():
        return TiberiusConfigParser.getParser().getboolean(ROBOT_ARM_SECTION, 'installed')

    '''******************************************
        Networking
    ******************************************'''

    @staticmethod
    def getIPAddress():
        ipa = TiberiusConfigParser.getParser().get(NETWORKING_SECTION, 'ip_address')
        return ipa

    @staticmethod
    def getName():
        name = TiberiusConfigParser.getParser().get(NETWORKING_SECTION, 'name')
        return name

    '''******************************************
        Steering
    ******************************************'''

    @staticmethod
    def getSteeringType():
        type = TiberiusConfigParser.getParser().get(STEERING_SECTION, 'type')
        return type

    '''******************************************
        Power
    ******************************************'''

    @staticmethod
    def getBatteryCapacity():
        capacity = TiberiusConfigParser.getParser().get(POWER_SECTION, 'capacity')
        return capacity

    @staticmethod
    def getBatteryChemistry():
        chemistry = TiberiusConfigParser.getParser().get(POWER_SECTION, 'chemistry')
        return chemistry

    '''******************************************
        Authentication
    ******************************************'''

    @staticmethod
    def getPassword():
        password = TiberiusConfigParser.getParser().get(AUTHENTICATION_SECTION, 'password')
        return password


if __name__ == "__main__":

    print TiberiusConfigParser.getIPAddress()
