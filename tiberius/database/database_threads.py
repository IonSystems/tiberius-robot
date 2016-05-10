import threading
import time
import traceback
import numpy as np

import update as up
import create as cr
import insert as ins
import query as q

from tiberius.config.config_parser import TiberiusConfigParser
from tiberius.database_wrapper.polyhedra_database import PolyhedraDatabase
from tables import UltrasonicsTable
from tables import GPSTable
from tables import CompassTable
from tables import ArmTable
from tables import LidarTable
from tables import MotorsTable
from tables import SteeringTable
from tables import SensorValidityTable
from tables import UltrasonicsValidityTable

# TODO: This 'ExternalHardwareController' would be be best split up into
# individual drivers as with cmps11, gps20 etc.
from tiberius.diagnostics.external_hardware_controller import ExternalHardwareController
from tiberius.diagnostics.external_hardware_controller import compass_monitor

from tiberius.control.sensors import Ultrasonic
from tiberius.control.sensors import GPS
if TiberiusConfigParser.isCompassEnabled():
    from tiberius.control.sensors import Compass
if TiberiusConfigParser.isLidarEnabled():
    from tiberius.control.sensors import Lidar
if TiberiusConfigParser.isMonitorEnabled():
    from tiberius.control.sensors import PowerManagementSensor

class DatabaseThreadCreator:
    '''
    Responsible for creating threads to populate the Polyhedra database
    with sensor data. A thread is created for each sensor. Each thread
    polls the sensor at a rate suitable for the particular sensor.
    Timestamps are included with each insert, to allow data to be queried
    based on age.

    On thread creation, a fresh database table is created, and any previous
    table and possible data is dropped.

    Actuator data is inserted at point of call using
    database.decorators.

    We avoid creating an instance of Control to prevent access to actuators.
    '''

    def __init__(self):
        # Used by every thread to insert into the database.
        self.poly = PolyhedraDatabase("insert_threads")

    def powermanagement_thread(self):
    	pow_man = PowerManagementSensor()
        powman_read_id = 0
    	while True:
            data = pow_man.getdata()
	    	#print pow_man.getdata()
            ins.insert_battery_reading(
                self.poly,
                powman_read_id,
                data)
            powman_read_id+=1


    '''******************************************
        Ultrasonics
    ******************************************'''

    def ultrasonics_thread(self):
        '''
        Repeatedly insert ultrasonics data into the database.
        '''
        ultrasonic = Ultrasonic()
        ultrasonic_read_id = 0
        valid = False

        while True:
            try:
                # TODO: Validity should not come from here, move validity checks
                # to validity module.
                ultra_data = ultrasonic.senseUltrasonic()
                validity = ultra_data['valid']

                if any(validity):
                    any_valid_data = True
                else:
                    any_valid_data = False

                # TODO: Something doesn't feel right here!
                if not valid:
                    valid = True
                up.update_ultrasonics_sensor_validity(self.poly, any_valid_data)

                up.update_ultrasonics_validity(self.poly, validity)

                # We need to put the data in, even if it is all 0's.
                # This gives a fail safe if a script was only relying on sensor data
                # and not using data validity
                ins.insert_ultrasonics_reading(
                    self.poly,
                    ultrasonic_read_id,
                    ultra_data
                )
                ultrasonic_read_id += 1
                time.sleep(0.2)
            except Exception as e:              # set to invalid
                if valid:
                    valid = False
                    up.update_ultrasonics_sensor_validity(self.poly, False)
                traceback.print_exc()
                print e

    '''******************************************
        GPS
    ******************************************'''

    def gps_thread(self):
        gps = GPS()
        gps_read_id = 0
        no_data_time = 0
        valid = False
        GPS_NUMBER_OF_READINGS = 10
        while True:
            try:
                if gps.usable():
                    gps_data = gps.read_gps()
                    gps_data['dilution_of_precision'] = -1
                    if gps_data is not False:
                        if gps_read_id < GPS_NUMBER_OF_READINGS:
                            ins.insert_gps_reading(self.poly, gps_read_id, gps_data)
                        else:  # start updating results
                            gps_update_id = gps_read_id % GPS_NUMBER_OF_READINGS
                            up.overwrite_gps_reading(self.poly, gps_update_id, gps_data)
                        if not valid:
                            valid = True
                            up.update_gps_sensor_validity(self.poly, True)
                        gps_read_id += 1
                        no_data_time = 0
                else:
                    # Wait till we have a gps fix before trying to insert data
                    time.sleep(0.1)
                    no_data_time += 0.1

                if no_data_time > 10:
                    if valid:
                        valid = False
                        up.update_gps_sensor_validity(self.poly, False)

            except Exception as e:
                traceback.print_exc()
                print e

    '''******************************************
        Compass
    ******************************************'''

    def compass_thread(self):
        compass = Compass()
        external_hardware_controller = ExternalHardwareController()
        compass_read_id = 0
        compass_update_id = 0
        valid = False
        previous_values = []
        COMPASS_NUMBER_OF_READINGS = 10
        while True:
            try:
                # get the compass heading
                heading = compass.headingNormalized()
                # TODO: Move validity checks to it's own module.

                # maintain a short array of previous values
                previous_values.append(heading)
                if len(previous_values) >= 10:
                    previous_values.pop(0)

                # ensure the compass heading has not changed too much between readings
                standard_deviation = np.std(np.diff(np.asarray(previous_values)))

                if standard_deviation > 10:
                    raise Exception('invalid data')
                else:
                    if compass_read_id < COMPASS_NUMBER_OF_READINGS: # store the first 10 results
                        ins.insert_compass_reading(self.poly, compass_read_id, heading)
                    else:  # start updating results
                        compass_update_id = compass_read_id % COMPASS_NUMBER_OF_READINGS
                        up.overwrite_compass_reading(self.poly, compass_update_id, heading)
                    compass_monitor(heading)
                    compass_read_id += 1

                # TODO: Again, something weird is going on here!
                # If not valid then valid = True?!
                if not valid:
                    valid = True
                    up.update_compass_sensor_validity(self.poly, True)

            except Exception as e:
                print e
                if valid:
                    valid = False
                    up.update_compass_sensor_validity(self.poly, False)
            time.sleep(0.5)

    '''******************************************
        Lidar
    ******************************************'''

    def lidar_thread(self):
        lidar_read_id = 0
        reading_iteration = 0
        l = Lidar()
        LIDAR_NUMBER_OF_READINGS = 100
        while True:
            data = l.get_filtered_lidar_data()
            for item in data:
                if reading_iteration < 5:
                    ins.insert_lidar_reading(self.poly, lidar_read_id, reading_iteration, item)
                else:
                    lidar_update_id = lidar_read_id % LIDAR_NUMBER_OF_READINGS
                    up.overwrite_lidar_reading(self.poly, lidar_update_id, reading_iteration, item)
                lidar_read_id += 1
            reading_iteration += 1
            time.sleep(0.5)

    '''******************************************
        Diagnostics
    ******************************************'''

    def diagnostics_thread(self, control):
        external_hardware_controller = control

        ultrasonics_status, compass_status, gps_status = False, False, False

        while True:
            try:
                rows = q.query_sensor_validity(self.poly)

                for row in rows:
                    ultrasonics_status = row.ultrasonics
                    compass_status = row.compass
                    gps_status = row.gps
                diagnostics_leds = {ultrasonics_status, compass_status, gps_status, 9, 9, 9, 9, 9}
                external_hardware_controller.set_hardware(diagnostics_leds)

            except Exception as e:
                print e
                traceback.print_exc()
            time.sleep(0.5)
