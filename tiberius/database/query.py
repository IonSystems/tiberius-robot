#!/usr/bin/python
from tiberius.database.polyhedra_database import PolyhedraDatabase
from tables import GPSTable
from tables import SensorValidityTable


'''
Contains useful queries that are called to get data from Tiberius's
in-memory database.
'''


def get_latest_gps(poly):
    '''
    Get the the latest valid gps reading.
    '''
    pass
    # result = self.db.query(Tables.GPS_TABLE)


def get_latest_ultrasonics(poly):
    '''
    Get the latest valid ultrasonics data.
    '''
    pass


def get_latest_lidar_reading(poly):
    '''
    Get the latest reading (around 360 points).
    '''
    pass


def get_latest_motor_speeds(poly):
    '''
    Get the latest speeds from all four motors.
    '''
    pass


def get_latest_steering_angles(poly):
    '''
    Get the latest steering angles for all four wheels.
    '''
    pass


def get_latest_compass_heading(poly):
    '''
    Get the latest compass heading value.
    '''
    pass


def query_sensor_validity(poly):
    return poly.query(
        SensorValidityTable.table_name,
        [
            'ultrasonics',
            'compass',
            'gps'
        ]
    )
