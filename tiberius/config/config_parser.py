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
GPS_SECTION = 'gps'
AUTHENTICATION_SECTION = 'authentication'
ARM_BASKET_SECTION = 'arm_basket_positions'
ARM_CENTRE_SECTION = 'arm_centre_positions'
ARM_PARK_SECTION = 'arm_park_positions'
ARM_HOME_SECTION = 'arm_home_positions'
DIAGNOSTICS_SECTION = 'diagnostics'

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

    @staticmethod
    def getLidarSerialPort():
        return TiberiusConfigParser.getParser().get(LIDAR_SECTION, 'serial_port')

    '''******************************************
        Motors
    ******************************************'''

    @staticmethod
    def areMotorsEnabled():
        return TiberiusConfigParser.getParser().getboolean(MOTORS_SECTION, 'installed')

    @staticmethod
    def getMotorInterface():
        return TiberiusConfigParser.getParser().get(MOTORS_SECTION, 'interface')

    @staticmethod
    def isI2C():
        return TiberiusConfigParser.getParser().get(MOTORS_SECTION, 'interface') == "I2C"

    @staticmethod
    def isUDP():
        return TiberiusConfigParser.getParser().get(MOTORS_SECTION, 'interface') == "UDP"

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

    @staticmethod
    def isArmCamEnabled():
        return TiberiusConfigParser.getParser().getboolean(ROBOT_ARM_SECTION, 'camera')

    @staticmethod
    def getArmSerialPort():
        return TiberiusConfigParser.getParser().get(ROBOT_ARM_SECTION, 'serial_port')

    '''******************************************
        GPS
    ******************************************'''

    @staticmethod
    def isGPSEnabled():
        return TiberiusConfigParser.getParser().getboolean(GPS_SECTION, 'installed')

    @staticmethod
    def getGPSSerialPort():
        return TiberiusConfigParser.getParser().get(GPS_SECTION, 'serial_port')

    '''******************************************
        diagnostics
    ******************************************'''

    @staticmethod
    def areDiagnosticsEnabled():
        return TiberiusConfigParser.getParser().getboolean(DIAGNOSTICS_SECTION, 'installed')


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

    @staticmethod
    def isMonitorEnabled():
        return TiberiusConfigParser.getParser().getboolean(POWER_SECTION, 'battery_monitor')

    @staticmethod
    def getBatteryMonitorPort():
        battery_port = TiberiusConfigParser.getParser().get(POWER_SECTION, 'battery_monitor_port')
        return battery_port

    @staticmethod
    def setBatteryMonitorPort(battery_port):
        TiberiusConfigParser.getParser().set(POWER_SECTION, battery_port)
        return battery_port


    '''******************************************
        Authentication
    ******************************************'''

    @staticmethod
    def getPassword():
        password = TiberiusConfigParser.getParser().get(AUTHENTICATION_SECTION, 'password')
        return password

    '''******************************************
        Arm Positions
    ******************************************'''

    @staticmethod
    def getArmParkParams():
        x = TiberiusConfigParser.getParser().getint(ARM_PARK_SECTION, 'x')
        y = TiberiusConfigParser.getParser().getint(ARM_PARK_SECTION, 'y')
        z = TiberiusConfigParser.getParser().getint(ARM_PARK_SECTION, 'z')
        return {'x': x, 'y': y, 'z': z}

    @staticmethod
    def getArmCentreParams():
        x = TiberiusConfigParser.getParser().getint(ARM_CENTRE_SECTION, 'x')
        y = TiberiusConfigParser.getParser().getint(ARM_CENTRE_SECTION, 'y')
        z = TiberiusConfigParser.getParser().getint(ARM_CENTRE_SECTION, 'z')
        return {'x': x, 'y': y, 'z': z}

    @staticmethod
    def getArmBasketParams():
        x = TiberiusConfigParser.getParser().getint(ARM_BASKET_SECTION, 'x')
        y = TiberiusConfigParser.getParser().getint(ARM_BASKET_SECTION, 'y')
        z = TiberiusConfigParser.getParser().getint(ARM_BASKET_SECTION, 'z')
        return {'x': x, 'y': y, 'z': z}

    @staticmethod
    def getArmHomeParams():
        x = TiberiusConfigParser.getParser().getint(ARM_HOME_SECTION, 'x')
        y = TiberiusConfigParser.getParser().getint(ARM_HOME_SECTION, 'y')
        z = TiberiusConfigParser.getParser().getint(ARM_HOME_SECTION, 'z')
        return {'x': x, 'y': y, 'z': z}


if __name__ == "__main__":

    print TiberiusConfigParser.getIPAddress()
    print TiberiusConfigParser.getArmParkParams()
    print TiberiusConfigParser.getArmCentreParams()
    print TiberiusConfigParser.getArmBasketParams()
