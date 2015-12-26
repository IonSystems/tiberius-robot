import ConfigParser

class TiberiusConfigParser():
    def __init__(self):
        self.parser = ConfigParser.ConfigParser()
        self.parser.read('configuration.conf')

    '''******************************************
        Constant values
    ******************************************'''
    INSTALLED = 'installed'
    LIDAR_SECTION = 'lidar'
    ULTRASONICS_SECTION = 'ultrasonics'
    STEERING_SECTION = 'steering'
    POWER_SECTION = 'power'
    NETWORKING_SECTION = 'networking'
    KINECT_SECTION = 'kinect'
    ROBOT_ARM_SECTION = 'arm'

    '''******************************************
        LIDAR
    ******************************************'''
    def isLidarEnabled(self):
        return self.parser.getBoolean(LIDAR_SECTION, 'installed')

    '''******************************************
        Ultrasonics
    ******************************************'''
    def getUltrasonicAddresses(self):
        front_centre = self.parser.get(ULTRASONICS_SECTION, 'front_centre')
        if(front_centre):
            items.append('front_centre')
        front_right = self.parser.get(ULTRASONICS_SECTION, 'front_right')
        if(front_right):
            items.append('front_right')
        front_left = self.parser.get(ULTRASONICS_SECTION, 'front_left')
        if(front_left):
            items.append('front_left')
        rear_centre = self.parser.get(ULTRASONICS_SECTION, 'rear_centre')
        if(rear_centre):
            items.append('rear_centre')
        rear_right = self.parser.get(ULTRASONICS_SECTION, 'rear_right')
        if(rear_right):
            items.append('rear_right')
        rear_left = self.parser.get(ULTRASONICS_SECTION, 'rear_left')
        if(rear_left):
            items.append('rear_left')
        return dict( (name,eval(name)) for name in items )

    '''******************************************
        Networking
    ******************************************'''
    def getIPAdress(self):
        ipa = self.parser.get(NETWORKING_SECTION, 'ip_address')
        return ipa
