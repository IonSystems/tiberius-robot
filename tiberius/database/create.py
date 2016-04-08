#!/usr/bin/python


def drop_create(poly, table):
    '''
    Drop a table then create it, this ensures the table has the latest column
    definitions and is initiall free of any data.
    '''
    try:
        poly.drop(table.table_name)
    except poly.NoSuchTableError:
        # Table didn't exist previously, no worries!
        pass
    try:
        poly.create(
            table.table_name,
            table.columns
        )
    except poly.OperationalError:
        print "something went wrong... "
    except poly.TableAlreadyExistsError:
        print table.table_name + " already exists."


def insert(poly, table, data):
    '''
    Insert into the Polyhedra database with protection from
    PolyhedraDatabase.OperationalError.
    '''
    try:
        poly.insert(SensorValidityTable.table_name, data)
    except poly.OperationalError:
        print table.table_name + " already exists."


def create_ultrasonics_table(poly):
    drop_create(poly, UltrasonicsTable)


def create_gps_table(poly):
    drop_create(poly, GPSTable)


def create_compass_tables(poly):
    drop_create(poly, CompassTable)


def polycreate_arm(poly):
    drop_create(poly, ArmTable)


def create_lidar_table(poly):
    drop_create(poly, LidarTable)


def create_motors_table(poly):
    drop_create(poly, MotorsTable)


def create_steering_table(self):
    drop_create(poly, SteeringTable)


def create_sensor_validity_table(self):
    '''
    This table is for overall sensor validity,
    individual validity is in a specific table for each sensor type.
    Although currently only ultrasonic validity tables are implemented.
    '''
    drop_create(poly, SensorValidityTable)
    data = {
        'id': 0,
        'ultrasonics': False,
        'compass': False,
        'gps': False,
        'timestamp': time.time()
    }
    insert(poly, SensorValidityTable, data)


def create_ultrasonics_validity_table(self):
    drop_insert(poly, UltrasonicsValidityTable)
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
