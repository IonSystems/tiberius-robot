#!/usr/bin/python
import time
from tables import UltrasonicsTable
from tables import GPSTable
from tables import CompassTable


def insert_ultrasonics_validity(poly, id, data):
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
    self.poly.insert(
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
    self.poly.insert(
        CompassTable.table_name,
        {
            'id': id,
            'heading': heading,
            'timestamp': time.time()
        }
    )


def insert_lidar_reading(poly, id, r_id, data):
    self.poly.insert(
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
