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
        {'gps': value}, {'clause': 'WHERE',
                        'data': [
                            {
                                'column': 'id',
                                'assertion': '=',
                                'value': '0'
                            }
                        ]})


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

