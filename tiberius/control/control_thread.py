import threading
import time
from tiberius.database.polyhedra_database import PolyhedraDatabase
from tiberius.control.sensors import Ultrasonic
from tiberius.control.sensors import Compass
from tiberius.control.sensors import GPS
import traceback
import numpy as np
'''
    Responsible for creating threads to communicate with the database, in order to control Tiberius.
'''


class ControlThread:
    def __init__(self):

        self.poly = PolyhedraDatabase("poly")
        self.ULTRASONICS_TABLE = 'ultrasonics_reading'
        self.COMPASS_TABLE = 'compass_reading'
        self.GPS_TABLE = 'gps_reading'
        self.ARM_TABLE = 'arm_reading'
        self.VALIDITY_TABLE = 'sensor_validity'
        self.VALIDITY_ULTRASONICS_TABLE = 'ultrasonics_validity'

    # *****************************Functions for creating the table*********************************
    # create polyhedra database to store data from ultrasonic sensors
    def polycreate_ultrasonic(self):
        try:
            self.poly.drop(self.ULTRASONICS_TABLE)
        except PolyhedraDatabase.NoSuchTableError:
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
        except PolyhedraDatabase.NoSuchTableError:
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
        except PolyhedraDatabase.NoSuchTableError:
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
        except PolyhedraDatabase.NoSuchTableError:
            print "Table doesn't exist"
        try:
            self.poly.create(self.VALIDITY_TABLE, {'id': 'int primary key',
                                                   'ultrasonics': 'bool',
                                                   'compass': 'bool',
                                                   'gps': 'bool',
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
        except PolyhedraDatabase.NoSuchTableError:
            print "Table doesn't exist"
        try:
            self.poly.create(self.VALIDITY_ULTRASONICS_TABLE, {'id': 'int primary key',
                                                               'fr': 'bool',
                                                               'fc': 'bool',
                                                               'fl': 'bool',
                                                               'rr': 'bool',
                                                               'rc': 'bool',
                                                               'rl': 'bool',
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
        ultrasonic = Ultrasonic()
        ultrasonic_read_id = 0
        valid = False

        while True:
            try:

                ultra_data = ultrasonic.senseUltrasonic()
                validity = ultra_data['valid']

                if any(validity):
                    any_valid_data = True
                else:
                    any_valid_data = False

                if not valid:
                    valid = True
                    self.poly.update(self.VALIDITY_TABLE, {'ultrasonics': any_valid_data},
                                     {'clause': 'WHERE',
                                      'data': [
                                          {
                                              'column': 'id',
                                              'assertion': '=',
                                              'value': '0'
                                          }
                                      ]})

                self.poly.update(self.VALIDITY_ULTRASONICS_TABLE, {'fr': validity[0],
                                                                   'fc': validity[1],
                                                                   'fl': validity[2],
                                                                   'rr': validity[3],
                                                                   'rc': validity[4],
                                                                   'rl': validity[5]},
                                 {'clause': 'WHERE',
                                  'data': [
                                      {
                                          'column': 'id',
                                          'assertion': '=',
                                          'value': '0'
                                      }
                                  ]})

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
            except Exception as e:              # set to invalid
                if valid:
                    valid = False
                    self.poly.update(self.VALIDITY_TABLE, {'ultrasonics': 0},
                                     {'clause': 'WHERE',
                                      'data': [
                                          {
                                              'column': 'id',
                                              'assertion': '=',
                                              'value': '0'
                                          }
                                      ]})
                traceback.print_exc()
                print e

    def gps_thread(self):
        gps = GPS()
        gps_read_id = 0
        no_data_time = 0
        valid = False
        while True:
            try:
                if gps.has_fix():
                    gps_data = gps.read_gps()
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
                        if not valid:
                            valid = True
                            self.poly.update(self.VALIDITY_TABLE, {'gps': True}, {'clause': 'WHERE',
                                                                               'data': [
                                                                                   {
                                                                                       'column': 'id',
                                                                                       'assertion': '=',
                                                                                       'value': '0'
                                                                                   }
                                                                               ]})

                        gps_read_id += 1
                        no_data_time = 0
                else:
                    # Wait till we have a gps fix before trying to insert data
                    time.sleep(0.1)
                    no_data_time += 0.1

                if no_data_time > 10:
                    if valid:
                        valid = False
                        self.poly.update(self.VALIDITY_TABLE, {'gps': False}, {'clause': 'WHERE',
                                                                           'data': [
                                                                               {
                                                                                   'column': 'id',
                                                                                   'assertion': '=',
                                                                                   'value': '0'
                                                                               }
                                                                           ]})

            except Exception as e:
                traceback.print_exc()
                print e

    def compass_thread(self):
        compass = Compass()
        compass_read_id = 0
        valid = False
        previous_values = []
        while True:
            try:
                # validate compass data by differentiating (shouldn't change too quickly)
                heading = compass.headingNormalized()
                # check if the compass data makes sense - common sense check

                previous_values.append(heading)
                if len(previous_values) >= 10:
                    previous_values.pop(0)

                standard_deviation = np.std(np.diff(np.asarray(previous_values)))
                if standard_deviation > 10:
                    raise Exception('invalid data')
                else:
                    self.poly.insert(self.COMPASS_TABLE,
                                     {'id': compass_read_id, 'heading': heading, 'timestamp': time.time()})

                    compass_read_id += 1

                if not valid:
                    valid = True
                    self.poly.update(self.VALIDITY_TABLE, {'compass': True}, {'clause': 'WHERE',
                                                                           'data': [
                                                                               {
                                                                                   'column': 'id',
                                                                                   'assertion': '=',
                                                                                   'value': '0'
                                                                               }
                                                                           ]})

            except Exception as e:
                print e
                if valid:
                    valid = False

                    self.poly.update(self.VALIDITY_TABLE, {'compass': False}, {'clause': 'WHERE',
                                                                           'data': [
                                                                               {
                                                                                   'column': 'id',
                                                                                   'assertion': '=',
                                                                                   'value': '0'
                                                                               }
                                                                           ]})
            time.sleep(0.5)
    
    def diagnostics_thread(self):
        from tiberius.diagnostics.diagnostics_leds import diagnostics_leds

        leds = diagnostics_leds()

        ultrasonics_status, compass_status, gps_status = False, False, False

        while True:
            try:
                rows = self.poly.query(self.VALIDITY_TABLE, ['ultrasonics', 'compass', 'gps'])
                print rows
                for row in rows:
                    print row
                    #ultrasonics_status = row.ultrasonics
                    #compass_status = row.compass
                    #gps_status = row.gps

                leds.setLEDs(ultrasonics_status, compass_status, gps_status)

            except Exception as e:
                print e
                traceback.print_exc()
            time.sleep(0.5)


            # **********************************Robotic arm - not currently implemented*********************
            # def arm_thread(self):
            #  arm_read_id = 0
            #  while(True):
            #        poly.insert(self.ARM_TABLE, {'id': arm_read_id, 'X': 'float', 'Y': 'float', 'Z' : 'float',
            #                                    'theta' : 'float', 'phi' : 'float', 'rho' : 'float',
            #                                    'timestamp':'float'})
            # arm_read_id += 1;
            # *********************************************************************************************************************
if __name__== "__main__":
    
    compass_thread()        
        
# for testing purposes - we call the functions.
# functions should be called as threads so they can run concurrently.
