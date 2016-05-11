#!/usr/bin/python
import time
from tables import SensorValidityTable
from tables import UltrasonicsValidityTable
from tables import UltrasonicsTable
from tables import GPSTable
from tables import CompassTable
from tables import ArmTable
from tables import LidarTable
from tables import MotorsTable
from tables import SteeringTable
from tables import GridTable
from tables import BatteryTable


def drop_create(poly, table):
    '''
    Drop a table then create it, this ensures the table has the latest column
    definitions and is initiall free of any data.
    '''
    try:
        poly.drop(table.table_name)
    except poly.NoSuchTableError:
        # Table didn't exist previously, no worries!
        pass
    try:
        poly.create(
            table.table_name,
            table.columns
        )
    except poly.OperationalError:
        print "something went wrong... "
    except poly.TableAlreadyExistsError:
        print table.table_name + " already exists."


def create_ultrasonics_table(poly):
    drop_create(poly, UltrasonicsTable)


def create_gps_table(poly):
    drop_create(poly, GPSTable)


def create_compass_table(poly):
    drop_create(poly, CompassTable)


def create_arm_table(poly):
    drop_create(poly, ArmTable)


def create_lidar_table(poly):
    drop_create(poly, LidarTable)


def create_motors_table(poly):
    drop_create(poly, MotorsTable)


def create_steering_table(poly):
    drop_create(poly, SteeringTable)

def create_battery_table(poly):
    drop_create(poly, BatteryTable)

def create_sensor_validity_table(poly):
    '''
    This table is for overall sensor validity,
    individual validity is in a specific table for each sensor type.
    Although currently only ultrasonic validity tables are implemented.
    '''
    drop_create(poly, SensorValidityTable)


def create_ultrasonics_validity_table(poly):
    drop_create(poly, UltrasonicsValidityTable)

def create_grid_table(poly):
    drop_create(poly, GridTable)
