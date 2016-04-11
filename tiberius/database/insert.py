#!/usr/bin/python
import time
from tables import UltrasonicsTable
from tables import GPSTable
from tables import CompassTable
from tables import LidarTable
from tables import SensorValidityTable
from tables import UltrasonicsValidityTable


def insert(poly, table, data):
    '''
    Insert into the Polyhedra database with protection from
    PolyhedraDatabase.OperationalError.
    '''
    try:
        poly.insert(table.table_name, data)
    except poly.OperationalError:
        print table.table_name + " already exists."


def insert_initial_sensor_validity(poly):
    data = {
        'id': 0,
        'ultrasonics': False,
        'compass': False,
        'gps': False,
        'timestamp': time.time()
    }
    insert(poly, SensorValidityTable, data)


def insert_initial_ultrasonics_validity(poly):
    data = {
        'id': 0,
        'fr': False,
        'fc': False,
        'fl': False,
        'rr': False,
        'rc': False,
        'rl': False,
        'timestamp': time.time()
    }
    insert(poly, UltrasonicsValidityTable, data)


def insert_ultrasonics_validity(poly, id, data):
    poly.insert(
        UltrasonicsValidityTable.table_name,
        {
            'id': id,
            'fr': data['fr'],
            'fc': data['fc'],
            'fl': data['fl'],
            'rr': data['rr'],
            'rc': data['rc'],
            'rl': data['rl'],
            'timestamp': time.time()})


def insert_ultrasonics_reading(poly, id, data):
    poly.insert(
        UltrasonicsTable.table_name,
        {
            'id': id,
            'fr': data['fr'],
            'fc': data['fc'],
            'fl': data['fl'],
            'rr': data['rr'],
            'rc': data['rc'],
            'rl': data['rl'],
            'timestamp': time.time()})


def insert_gps_reading(poly, id, data):
    poly.insert(
        GPSTable.table_name,
        {
            'id': id,
            'latitude': data['latitude'],
            'longitude': data['longitude'],
            'gls_qual': data['gls_qual'],
            'num_sats': data['num_sats'],
            'dilution_of_precision': data['dilution_of_precision'],
            'velocity': data['velocity'],
            'fixmode': data['fixmode'],
            'timestamp': time.time()
        }
    )


def insert_compass_reading(poly, id, heading):
    poly.insert(
        CompassTable.table_name,
        {
            'id': id,
            'heading': heading,
            'timestamp': time.time()
        }
    )


def insert_lidar_reading(poly, id, r_id, data):
    poly.insert(
        LidarTable.table_name,
        {
            'id': id,
            'reading_iteration': r_id,
            'start_flag': data['start_flag'],
            'angle': data['theta'],
            'distance': data['dist'],
            'quality': data['quality'],
            'timestamp': time.time()
        }
    )
