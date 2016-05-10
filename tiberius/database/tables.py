#!/usr/bin/python
import abc
from tiberius.database_wrapper.table import Table


class UltrasonicsTable(Table):
    table_name = "ultrasonics_reading"
    columns = {
        'id': 'int primary key',
        'fl': 'float',
        'fc': 'float',
        'fr': 'float',
        'rl': 'float',
        'rc': 'float',
        'rr': 'float',
        'timestamp': 'float'
    }


class GPSTable(Table):
    table_name = "gps_reading"
    columns = {
        'id': 'int primary key',
        'latitude': 'float',
        'longitude': 'float',
        'altitude': 'float',
        'gps_qual': 'int',
        'num_sats': 'int',
        'dilution_of_precision': 'float',
        'velocity': 'float',
        'fixmode': 'int',
        'timestamp': 'float'}


class CompassTable(Table):
    table_name = "compass_reading"
    columns = {
        'id': 'int primary key',
        'heading': 'float',
        'tilt': 'float',
        'pitch': 'float',
        'roll': 'float',
        'temperature': 'float',
        'timestamp': 'float'}


class ArmTable(Table):
    table_name = "arm_positions"
    columns = {
        'id': 'int primary key',
        'X': 'float',
        'Y': 'float',
        'Z': 'float',
        'waist': 'float',
        'elbow': 'float',
        'shoulder': 'float',
        'timestamp': 'float'
    }


class LidarTable(Table):
    table_name = "lidar_reading"
    columns = {
        'id': 'int primary key',
        'start_flag': 'varchar',
        'angle': 'float',
        'distance': 'float',
        'quality': 'float',
        'reading_iteration': 'int',
        'timestamp': 'float'
    }

class MotorsTable(Table):
    table_name = "motors_table"
    columns = {
        'id': 'int primary key',
        'front_left': 'float',
        'front_right': 'float',
        'rear_left': 'float',
        'rear_right': 'float',
        'timestamp': 'float'
    }


class SteeringTable(Table):
    table_name = "steering_table"
    columns = {
        'id': 'int primary key',
        'front_left': 'float',
        'front_right': 'float',
        'rear_left': 'float',
        'rear_right': 'float',
        'timestamp': 'float'
    }

class BatteryTable(Table):
    table_name = "battery_reading"
    columns = {
        'id': 'int primary key',
        'monitor': 'int',
        'volts': 'float',
        'current': 'float',
        'power': 'float',
        'time': 'float',
        'amp_hours': 'float',
        'watt_hours': 'float',
        'timestamp': 'float'
    }
'''
Alright, now the following tables have been refactored into this Table format,
but I can't see these being very useful. Cameron
'''


class SensorValidityTable(Table):
    table_name = "sensors_validity"
    columns = {
        'id': 'int primary key',
        'ultrasonics': 'bool',
        'compass': 'bool',
        'gps': 'bool',
        'timestamp': 'float'
    }


class UltrasonicsValidityTable(Table):
    table_name = "ultrasonics_validity"
    columns = {
        'id': 'int primary key',
        'fr': 'bool',
        'fc': 'bool',
        'fl': 'bool',
        'rr': 'bool',
        'rc': 'bool',
        'rl': 'bool',
        'timestamp': 'float'
    }

class GridTable(Table):
    table_name = "grid_table"
    columns = {
        'id': 'int primary key',
        'row': 'int',
        'column': 'int',
        'lat': 'float',
        'lon': 'float',
        'cost': 'int',
        'heuristic': 'int',
        'final': 'int',
        'parent': 'int primary key',
        'timestamp': 'float'
    }
