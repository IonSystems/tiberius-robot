#!/usr/bin/python
from tiberius.database_wrapper.polyhedra_database import PolyhedraDatabase
from tables import SensorValidityTable


'''
Contains useful queries that are called to get data from Tiberius's
in-memory database.
'''


def get_latest(poly, table, limit=1):

    query = "SELECT * from " + table.table_name + " LIMIT " + str(limit) + ";"  # ORDER BY timestamp DESC
    print query
    return poly.sql(query)


def query_sensor_validity(poly):
    return poly.query(
        SensorValidityTable.table_name,
        [
            'ultrasonics',
            'compass',
            'gps'
        ]
    )
