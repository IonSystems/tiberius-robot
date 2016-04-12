import time
from tables import UltrasonicsTable
from tables import GPSTable
from tables import CompassTable
from tables import LidarTable
from tables import SensorValidityTable
from tables import UltrasonicsValidityTable


def update_ultrasonics_sensor_validity(poly, valid):
    '''
    Update the ultrasonics validity boolean value.
    '''
    poly.update(
        SensorValidityTable.table_name,
        {
            'ultrasonics': valid
        },
        {
            'clause': 'WHERE',
            'data': [
                {
                    'column': 'id',
                    'assertion': '=',
                    'value': '0'
                }
            ]
        }
    )


def update_gps_sensor_validity(poly, value):
    poly.update(
        SensorValidityTable.table_name,
        {
            'gps': value
        },
        {
            'clause': 'WHERE',
            'data': [
                            {
                                'column': 'id',
                                'assertion': '=',
                                'value': '0'
                            }
                        ]
                    }
                )


def update_ultrasonics_validity(poly, validity):
    poly.update(
        UltrasonicsValidityTable.table_name,
        {
            'fr': validity[0],
            'fc': validity[1],
            'fl': validity[2],
            'rr': validity[3],
            'rc': validity[4],
            'rl': validity[5]
        },
        {
            'clause': 'WHERE',
            'data': [
                {
                    'column': 'id',
                    'assertion': '=',
                    'value': '0'
                }
            ]
        }
    )


def update_compass_sensor_validity(poly, value):
    poly.update(
        SensorValidityTable.table_name,
        {
            'compass': value
        },
        {
            'clause': 'WHERE',
            'data': [
                {
                    'column': 'id',
                    'assertion': '=',
                    'value': '0'
                }
            ]
        }
    )


def overwrite_ultrasonics_reading(poly, id, data):
    '''******************************************
        Ultrasonics
    ******************************************'''
    poly.update(
        SensorValidityTable.table_name,
        {
            # 'id': id,
            'fr': data['fr'],
            'fc': data['fc'],
            'fl': data['fl'],
            'rr': data['rr'],
            'rc': data['rc'],
            'rl': data['rl'],
            'timestamp': time.time()
        },
        {
            'clause': 'WHERE',
            'data': [
                {
                    'column': 'id',
                    'assertion': '=',
                    'value': id
                }
            ]
        }
    )


def overwrite_gps_reading(poly, id, data):
    '''******************************************
        GPS
    ******************************************'''
    poly.update(
        CompassTable.table_name,
        {
            # 'id': id,
            'latitude': data['latitude'],
            'longitude': data['longitude'],
            'gps_qual': data['gps_qual'],
            'num_sats': data['num_sats'],
             # 'dilution_of_precision': data['dilution_of_precision'],  #having problem updating this
            'velocity': data['velocity'],
            # 'fixmode': data['fixmode'], #same problem as above
            'timestamp': time.time()
        },
        {
            'clause': 'WHERE',
            'data': [
                {
                    'column': 'id',
                    'assertion': '=',
                    'value': id
                }
            ]
        }
    )


def overwrite_compass_reading(poly, id, value):
    '''******************************************
        Compass
    ******************************************'''
    poly.update(
        CompassTable.table_name,
        {
            'compass': value,
            'timestamp': time.time()
        },
        {
            'clause': 'WHERE',
            'data': [
                {
                    'column': 'id',
                    'assertion': '=',
                    'value': id
                }
            ]
        }
    )


def overwrite_lidar_reading(poly, id, r_id, data):
    '''******************************************
        Lidar
    ******************************************'''
    poly.update(
        CompassTable.table_name,
        {
            # 'id': id,
            'reading_iteration': r_id,
            'start_flag': data['start_flag'],
            'angle': data['theta'],
            'distance': data['dist'],
            'quality': data['quality'],
            'timestamp': time.time()
        },
        {
            'clause': 'WHERE',
            'data': [
                {
                    'column': 'id',
                    'assertion': '=',
                    'value': id
                }
            ]
        }
    )
