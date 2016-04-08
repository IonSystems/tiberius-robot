import threading
import time
import traceback
import numpy as np

import tiberius.database.update as up
import tiberius.database.create as cr

from tiberius.config.config_parser import TiberiusConfigParser
from tiberius.database.polyhedra_database import PolyhedraDatabase
from tiberius.database.tables import UltrasonicsTable
from tiberius.database.tables import GPSTable
from tiberius.database.tables import CompassTable
from tiberius.database.tables import ArmTable
from tiberius.database.tables import LidarTable
from tiberius.database.tables import MotorsTable
from tiberius.database.tables import SteeringTable
from tiberius.database.tables import SensorValidityTable
from tiberius.database.tables import UltrasonicsValidityTable
from tiberius.control.sensors import Ultrasonic
if TiberiusConfigParser.isCompassEnabled():
    from tiberius.control.sensors import Compass
if TiberiusConfigParser.isLidarEnabled():
    from tiberius.control.sensors import Lidar
from tiberius.control.sensors import GPS


class DatabaseThreadCreator:
    '''
        Responsible for creating threads to populate the Polyhedra database
        with sensor data. A thread is created for each sensor. Each thread polls
        the sensor at a rate suitable for the particular sensor. Timestamps are
        included with each insert, to allow data to be queried based on age.

        On thread creation, a fresh database table is created, and any previous
        table and possible data is dropped.

        Actuator data is inserted at point of call using
        database.decorators.
    '''
    def __init__(self):
        # Used by every thread to insert into the database.
        self.poly = PolyhedraDatabase("insert_threads")

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
                up.update_sensor_validity(any_data_valid)

                up.update_ultrasonics_validity(self.poly, ultra_data)

                # We need to put the data in, even if it is all 0's.
                # This gives a fail safe if a script was only relying on sensor data
                # and not using data validity
                ins.insert_ultrasonic_validity(
                    self.poly,
                    ultrasonic_read_id,
                    ultra_data
                )
                ultrasonic_read_id += 1
                time.sleep(0.2)
            except Exception as e:              # set to invalid
                if valid:
                    valid = False
                    up.update_ultrasonics_sensor_validity(poly, False)
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
                        self.poly.insert(GPSTable.table_name, {'id': gps_read_id,
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
                            self.poly.update(SensorValidityTable.table_name, {'gps': True}, {'clause': 'WHERE',
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
                        self.poly.update(SensorValidityTable.table_name, {'gps': False}, {'clause': 'WHERE',
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
                    self.poly.insert(CompassTable.table_name,
                                     {'id': compass_read_id, 'heading': heading, 'timestamp': time.time()})

                    compass_read_id += 1

                if not valid:
                    valid = True
                    self.poly.update(SensorValidityTable.table_name, {'compass': True}, {'clause': 'WHERE',
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

                    self.poly.update(SensorValidityTable.table_name, {'compass': False}, {'clause': 'WHERE',
                                                                           'data': [
                                                                               {
                                                                                   'column': 'id',
                                                                                   'assertion': '=',
                                                                                   'value': '0'
                                                                               }
                                                                           ]})
            time.sleep(0.5)


    def lidar_thread(self):
        lidar_read_id = 0
        reading_iteration = 0
        l = Lidar()
        while True:
            data = l.get_filtered_lidar_data()
            for item in data:
                self.poly.insert(LidarTable.table_name, {
                    'id': lidar_read_id,
                    'start_flag': item['start_flag'],
                    'angle':item['theta'],
                    'distance': item['dist'],
                    'quality': item['quality'],
                    'reading_iteration' : reading_iteration,
                    'timestamp': time.time()
                })
                lidar_read_id += 1
            reading_iteration += 1
            time.sleep(0.5)



    def diagnostics_thread(self):
        from tiberius.diagnostics.external_hardware_controller import ExternalHardwareController

        external_hardware_controller = ExternalHardwareController()

        ultrasonics_status, compass_status, gps_status = False, False, False

        while True:
            try:
                rows = self.poly.query(SensorValidityTable.table_name, ['ultrasonics', 'compass', 'gps'])
                print rows
                for row in rows:
                    print row
                    #ultrasonics_status = row.ultrasonics
                    #compass_status = row.compass
                    #gps_status = row.gps
                diagnostics_leds = {ultrasonics_status, compass_status, gps_status, -1, -1, -1, -1, -1}
                external_hardware_controller.set_hardware(diagnostics_leds)

            except Exception as e:
                print e
                traceback.print_exc()
            time.sleep(0.5)
