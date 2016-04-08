#!/usr/bin/python
import time


def insert_ultrasonics_validity(poly, id, data):
    poly.insert(
        UltrasonicsTable.table_name,
        {
            'id': id,
            'fr': ultra_data['fr'],
            'fc': ultra_data['fc'],
            'fl': ultra_data['fl'],
            'rr': ultra_data['rr'],
            'rc': ultra_data['rc'],
            'rl': ultra_data['rl'],
            'timestamp': time.time()})
