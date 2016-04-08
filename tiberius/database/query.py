#!/usr/bin/python
from tiberius.database.polyhedra_database import PolyhedraDatabase
from tiberius.database.tables import Tables


class Query:
    '''
    Contains useful queries that are called to get data from Tiberius's
    in-memory database.
    '''
    def __init__(self):
        self.db = PolyhedraDatabase("query_instance")

    def get_latest_gps(self):
        '''
        Get the the latest valid gps reading.
        '''
        pass
        #result = self.db.query(Tables.GPS_TABLE)

    def get_latest_ultrasonics(self):
        '''
        Get the latest valid ultrasonics data.
        '''
        pass

    def get_latest_lidar_reading(self):
        '''
        Get the latest reading (around 360 points).
        '''
        pass

    def get_latest_motor_speeds(self):
        '''
        Get the latest speeds from all four motors.
        '''
        pass

    def get_latest_steering_angles(self):
        '''
        Get the latest steering angles for all four wheels.
        '''
        pass

    def get_latest_compass_heading(self):
        '''
        Get the latest compass heading value.
        '''
        pass
