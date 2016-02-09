import thread
import time
from tiberius.database.polyhedra_database import PolyhedraDatabase
from tiberius.control.sensors import Ultrasonic
from tiberius.control.sensors import Compass
#from tiberius.control.sensors import GPS


#hello


'''
    Responsible for creating threads to communicate with the database, in order to control Tiberius.
'''


class ControlThread():

    def __init__(
            self,
            motor_control=True,
            lighting_control=True,
            gps_control=True,
            lidar_control=True,
            keyboard_control=True,
            compass_control=True,
            ultrasonic_control=True):
        # Find out what threads need to be created.
        self.motor_control = motor_control
        self.lighting_control = lighting_control
        self.gps_control = gps_control
        self.lidar_control = lidar_control
        self.keyboard_control = keyboard_control
        self.compass_control = compass_control
        self.ultrasonic_control = ultrasonic_control
        self.poly = PolyhedraDatabase("poly")
        self.ULTRASONICS_TABLE = 'ultrasonics_reading'
        self.COMPASS_TABLE = 'compass_reading'
        self.GPS_TABLE = 'gps_reading'
        self.ARM_TABLE = 'arm_reading'
        self.ultrasonic = Ultrasonic()


#*****************************Functions for creating the table*********************************
#create polyhedra database to store data from ultrasonic sensors
    def polycreate_ultrasonic(self):
        try:

            self.poly.create(self.ULTRASONICS_TABLE, {'id':'int primary key','fl': 'float',
                                               'fc': 'float', 'fr': 'float',
                                               'rl': 'float', 'rc': 'float',
                                               'rr': 'float',
                                               'timestamp':'float'})
        except PolyhedraDatabase.OperationalError:
            print "something went wrong... "
        except PolyhedraDatabase.TableAlreadyExistsError as e:
            print "Table already exists."

    def polycreate_gps(self):
        try:
            self.poly.create(self.GPS_TABLE, {'id':'int primary key', 'latitude':'float', 'longitude':'float',
                                         'north_south' : 'bool', 'east_west' : 'bool', 'altitude' : 'float',
                                         'variation' : 'float', 'velocity' : 'float', 'timestamp':'float'})
        except PolyhedraDatabase.TableAlreadyExistsError as e:
            print "Table already exists."
        except PolyhedraDatabase.OperationalError:
            print "GPS table already exists"

    def polycreate_compass(self):
        try:

            self.poly.create(self.COMPASS_TABLE, {'id':'int primary key', 'heading':'float', 'timestamp' : 'float'})
        except PolyhedraDatabase.TableAlreadyExistsError as e:
            print "Table already exists."
        except PolyhedraDatabase.OperationalError:
            print "Compass table already exists"


    def polycreate_arm(self):
        try:
            self.poly.create(self.ARM_TABLE, {'id':'int primary key', 'X': 'float', 'Y': 'float', 'Z' : 'float',
                                         'theta' : 'float', 'phi' : 'float', 'rho' : 'float',
                                         'timestamp':'float' })
        except PolyhedraDatabase.TableAlreadyExistsError as e:
            print "Table already exists."
        except PolyhedraDatabase.OperationalError:
            print "Arm table already exists"



#*****************************Functions for updating the table*********************************
    def ultrasonics_thread(self):
        ultrasonic_read_id = 0
        while(True):
            #add in code to update table by overwriting 0th value and rolling back round
            ultra_data = self.ultrasonic.senseUltrasonic()
            self.poly.insert(self.ULTRASONICS_TABLE, {'id' :ultrasonic_read_id,
                                                 'fl': ultra_data ['fl'], 'fc': ultra_data ['fc'],'fr': ultra_data ['fr'],
                                                 'rl': ultra_data ['rl'],'rc': ultra_data ['rc'], 'rr': ultra_data ['rr'],
                                                 'timestamp': time.time()} )
            ultrasonic_read_id += 1
            time.sleep(0.2)

    def gps_thread(self):
        gps_read_id = 0
        while(True):
            gps_data = GPS.read_gps(self)
            self.poly.insert(self.GPS_TABLE, {'id' : gps_read_id, 'latitude':  gps_data ['latitude'], 'longitude':
                                            gps_data ['longitude'], 'north_south' : gps_data['northsouth'],
                                            'east_west' : gps_data['eastwest'], 'altitude' : gps_data['altitude'],
                                            'variation' : gps_data['variation'], 'velocity' : gps_data['velocity'],
                                            'timestamp': time.time()} )
            gps_read_id += 1


    def compass_thread(self):
        compass_read_id = 0
        while(True):
            heading  = Compass.headingNormalized(self)
            self.poly.insert(self.COMPASS_TABLE, {'id': compass_read_id , 'heading': 'heading','timestamp': time.time()})

            compass_read_id += 1

#def arm_thread(self):
  #  arm_read_id = 0
  #  while(True):
#        poly.insert(self.ARM_TABLE, {'id': arm_read_id, 'X': 'float', 'Y': 'float', 'Z' : 'float',
 #                                    'theta' : 'float', 'phi' : 'float', 'rho' : 'float',
 #                                    'timestamp':'float'})
#    arm_read_id += 1;


if __name__ == "__main__":
    control_thread = ControlThread()
    control_thread.polycreate_ultrasonic()
    control_thread.ultrasonics_thread()
