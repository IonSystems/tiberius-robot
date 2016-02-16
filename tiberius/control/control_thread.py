import threading
import time
from tiberius.database.polyhedra_database import PolyhedraDatabase
from tiberius.control.sensors import Ultrasonic
from tiberius.control.sensors import Compass
from tiberius.control.sensors import GPS

'''
    Responsible for creating threads to communicate with the database, in order to control Tiberius.
'''


class ControlThread(threading.Thread):
    def __init__(self):

        self.poly = PolyhedraDatabase("poly")
        self.ULTRASONICS_TABLE = 'ultrasonics_reading'
        self.COMPASS_TABLE = 'compass_reading'
        self.GPS_TABLE = 'gps_reading'
        self.ARM_TABLE = 'arm_reading'
        self.VALIDITY_TABLE = 'sensor_validity'
        self.VALIDITY_ULTRASONICS_TABLE = 'ultrasonics_validity'
        self.ultrasonic = Ultrasonic()
        self.compass = Compass()
        self.gps = GPS()

    # *****************************Functions for creating the table*********************************
    # create polyhedra database to store data from ultrasonic sensors
    def polycreate_ultrasonic(self):
        try:
            self.poly.drop(self.ULTRASONICS_TABLE)
        except:
            print "Table doesn't exist"
        try:

            self.poly.create(self.ULTRASONICS_TABLE, {'id': 'int primary key',
                                                      'fl': 'float',
                                                      'fc': 'float',
                                                      'fr': 'float',
                                                      'rl': 'float',
                                                      'rc': 'float',
                                                      'rr': 'float',
                                                      'timestamp': 'float'})
        except PolyhedraDatabase.OperationalError:
            print "something went wrong... "
        except PolyhedraDatabase.TableAlreadyExistsError:
            print "Table already exists."

    def polycreate_gps(self):
        try:
            self.poly.drop(self.GPS_TABLE)
        except:
            print "Table doesn't exist"
        try:
            self.poly.create(self.GPS_TABLE, {'id': 'int primary key',
                                              'latitude': 'float',
                                              'longitude': 'float',
                                              'gls_qual': 'int',
                                              'num_sats': 'int',
                                              'dilution_of_precision': 'float',
                                              'velocity': 'float',
                                              'fixmode': 'int',
                                              'timestamp': 'float'})
        except PolyhedraDatabase.TableAlreadyExistsError:
            print "Table already exists."
        except PolyhedraDatabase.OperationalError:
            print "GPS table already exists"

    def polycreate_compass(self):
        try:
            self.poly.drop(self.COMPASS_TABLE)
        except:
            print "Table doesn't exist"
        try:

            self.poly.create(self.COMPASS_TABLE, {'id': 'int primary key', 'heading': 'float', 'timestamp': 'float'})
        except PolyhedraDatabase.TableAlreadyExistsError:
            print "Table already exists."
        except PolyhedraDatabase.OperationalError:
            print "Compass table already exists"

    def polycreate_arm(self):
        try:
            self.poly.create(self.ARM_TABLE, {'id': 'int primary key', 'X': 'float', 'Y': 'float', 'Z': 'float',
                                              'theta': 'float', 'phi': 'float', 'rho': 'float',
                                              'timestamp': 'float'})
        except PolyhedraDatabase.TableAlreadyExistsError:
            print "Table already exists."
        except PolyhedraDatabase.OperationalError:
            print "Arm table already exists"

    # This table is for overall sensor validity, individual validity is in a specific table for each sensor type.
    def polycreate_sensor_validity(self):
        try:
            self.poly.drop(self.VALIDITY_TABLE)
        except:
            print "Table doesn't exist"
        try:
            self.poly.create(self.VALIDITY_TABLE, {'id': 'int primary key',
                                                   'ultrasonics': 'int',
                                                   'compass': 'int',
                                                   'gps': 'int',
                                                   'timestamp': 'float'})

            self.poly.insert(self.VALIDITY_TABLE, {'id': 0,
                                                   'ultrasonics': 0,
                                                   'compass': 0,
                                                   'gps': 0,
                                                   'timestamp': time.time()})
        except PolyhedraDatabase.TableAlreadyExistsError:
            print "Table already exists."
        except PolyhedraDatabase.OperationalError:
            print "Sensor validity table already exists"

    def polycreate_ultrasonics_validity(self):
        try:
            self.poly.drop(self.VALIDITY_ULTRASONICS_TABLE)
        except:
            print "Table doesn't exist"
        try:
            self.poly.create(self.VALIDITY_ULTRASONICS_TABLE, {'id': 'int primary key',
                                                               'fr': 'int',
                                                               'fc': 'int',
                                                               'fl': 'int',
                                                               'rr': 'int',
                                                               'rc': 'int',
                                                               'rl': 'int',
                                                               'timestamp': 'float'})

            self.poly.insert(self.VALIDITY_ULTRASONICS_TABLE, {'id': 0,
                                                               'fr': '0',
                                                               'fc': '0',
                                                               'fl': '0',
                                                               'rr': '0',
                                                               'rc': '0',
                                                               'rl': '0',
                                                               'timestamp': time.time()})
        except PolyhedraDatabase.TableAlreadyExistsError:
            print "Table already exists."
        except PolyhedraDatabase.OperationalError:
            print "Ultrasonics validity table already exists"


        # *****************************Functions for updating the table*********************************

    def ultrasonics_thread(self):
        ultrasonic_read_id = 0
        while True:
            # TODO: add in code to update table by overwriting 0th value and rolling back round

            ultra_data = self.ultrasonic.senseUltrasonic()

            any_valid_data = 0
            validity = [6]
            for i in range(0, 5):
                if ultra_data['valid'][i] is False:
                    validity[i] = 0
                else:
                    validity[i] = 1
                    any_valid_data = 1

            self.poly.update(self.VALIDITY_TABLE, {'ultrasonics': any_valid_data},
                             {'id': 0})

            self.poly.update(self.VALIDITY_ULTRASONICS_TABLE, {'fr': validity[0],
                                                               'fc': validity[1],
                                                               'fl': validity[2],
                                                               'rr': validity[3],
                                                               'rc': validity[4],
                                                               'rl': validity[5]},
                             {'id': 0})

            # We need to put the data in, even if it is all 0's.
            # This gives a fail safe if a script was only relying on sensor data
            # and not using data validity
            self.poly.insert(self.ULTRASONICS_TABLE, {'id': ultrasonic_read_id,
                                                      'fr': ultra_data['fr'],
                                                      'fc': ultra_data['fc'],
                                                      'fl': ultra_data['fl'],
                                                      'rr': ultra_data['rr'],
                                                      'rc': ultra_data['rc'],
                                                      'rl': ultra_data['rl'],
                                                      'timestamp': time.time()})
            ultrasonic_read_id += 1
            time.sleep(0.2)

    def gps_thread(self):
        gps_read_id = 0
        no_data_time = 0
        while True:
            if self.gps.has_fix():
                gps_data = self.gps.read_gps()
                if gps_data is not False:
                    self.poly.insert(self.GPS_TABLE, {'id': gps_read_id,
                                                      'latitude': gps_data['latitude'],
                                                      'longitude': gps_data['longitude'],
                                                      'gls_qual': gps_data['gls_qual'],
                                                      'num_sats': gps_data['num_sats'],
                                                      'dilution_of_precision': gps_data['dilution_of_precision'],
                                                      'velocity': gps_data['velocity'],
                                                      'fixmode': gps_data['fixmode'],
                                                      'timestamp': time.time()})
                    self.poly.update(self.VALIDITY_TABLE, {'gps': 1}, {'id': 0})
                    gps_read_id += 1
                    no_data_time = 0
            else:
                # Wait till we have a gps fix before trying to insert data
                time.sleep(0.1)
                no_data_time += 0.1

            if no_data_time > 10:
                self.poly.update(self.VALIDITY_TABLE, {'gps': 0}, {'id': 0})

    def compass_thread(self):
        compass_read_id = 0
        while True:
            heading = self.compass.headingNormalized()
            self.poly.insert(self.COMPASS_TABLE, {'id': compass_read_id, 'heading': heading, 'timestamp': time.time()})

            compass_read_id += 1

    # **********************************Robotic arm - not currently implemented*********************
    # def arm_thread(self):
    #  arm_read_id = 0
    #  while(True):
    #        poly.insert(self.ARM_TABLE, {'id': arm_read_id, 'X': 'float', 'Y': 'float', 'Z' : 'float',
    #                                    'theta' : 'float', 'phi' : 'float', 'rho' : 'float',
    #                                    'timestamp':'float'})
    # arm_read_id += 1;
    # ******************************************************************************************************************************

# for testing purposes - we call the functions.
# functions should be called as threads so they can run concurrently.

if __name__ == "__main__":
    control_thread = ControlThread()
    control_thread.polycreate_sensor_validity()
    control_thread.polycreate_ultrasonic()  # set up the ultrasonic table
    control_thread.polycreate_compass()
    control_thread.polycreate_gps()


    threading.Thread(target=control_thread.ultrasonics_thread).start()
    threading.Thread(target=control_thread.compass_thread).start()
    #   threading.Thread(target = control_thread.gps_thread).start()
