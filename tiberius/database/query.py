#!/usr/bin/python
from tiberius.database.polyhedra_database import PolyhedraDatabase
from tables import SensorValidityTable


'''
Contains useful queries that are called to get data from Tiberius's
in-memory database.
'''


def get_latest(poly, table):
    return poly.sql("SELECT * from " + table.table_name + " ORDER BY timestamp DESC LIMIT 1;")


def query_sensor_validity(poly):
    return poly.query(
        SensorValidityTable.table_name,
        [
            'ultrasonics',
            'compass',
            'gps'
        ]
    )
