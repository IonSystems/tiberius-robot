#!/usr/bin/python
from tiberius.database_wrapper.polyhedra_database import PolyhedraDatabase
from tables import SensorValidityTable


'''
Contains useful queries that are called to get data from Tiberius's
in-memory database.
'''


def get_latest(poly, table, limit=1):
    return poly.sql("SELECT * from " + table.table_name + " ORDER BY timestamp DESC LIMIT " + str(limit) + ";")


def query_sensor_validity(poly):
    return poly.query(
        SensorValidityTable.table_name,
        [
            'ultrasonics',
            'compass',
            'gps'
        ]
    )
