#!/usr/bin/python


import time
from tables import ArmTable
from tables import MotorsTable
from tiberius.database_wrapper.polyhedra_database import PolyhedraDatabase
from tiberius.control.states import MotorState


db = PolyhedraDatabase("decorator_instance")

# We have not currently implemented autoincrementing keys,
# so we need to keep track of the key explicitly
arm_read_id = 0
motor_read_id = 0
grid_read_id = 0


def database_arm_update(func):

    '''
        After each arm movement function call,
        ensure that the arm positions are stored
        in the database.
    '''
    global arm_read_id

    def func_wrapper(self, change, angle=None):
        global arm_read_id
        # Call the originating function first,
        # so that the instance fields are up to date.
        result = func(self, change, angle=None)

        # Update the database with values from self
        try:
            db.insert(ArmTable.table_name, {
                'id': arm_read_id,
                'X': self.x,
                'Y': self.y,
                'Z' : self.z,
                'waist': self.waist_angle,
                'elbow': self.elbow_angle,
                'shoulder': self.shoulder_angle,
                'timestamp': time.time()

            })
            arm_read_id += 1
        except PolyhedraDatabase.UnknownError:
            print "Arm database entry failed."
    return func_wrapper


def database_motor_update(func):

    '''
        Update database after a motor command.
    '''
    global motor_read_id

    def func_wrapper(self, *args, **kwargs):
        global motor_read_id
        # Call the originating function first,
        # so that the instance fields are up to date.
        result = func(self, *args, **kwargs)

        # The information we need will either be in args,
        # or extrapolated from motor state.
        if len(args) == 2:
            front_left = args[0]
            rear_left = args[0]
            front_right = args[1]
            rear_right = args[1]
        elif len(args) == 4:
            front_left = args[0]
            rear_left = args[2]
            front_right = args[1]
            rear_right = args[3]
        else:
            # Get speeds using motor state and self
            # could be cleaned down
            if self.state == MotorState.FORWARD:
                front_left = self.speed
                rear_left = self.speed
                front_right = self.speed
                rear_right = self.speed
            elif self.state == MotorState.BACKWARD:
                front_left = -self.speed
                rear_left = -self.speed
                front_right = -self.speed
                rear_right = -self.speed
            elif self.state == MotorState.LEFT:
                front_left = -self.speed
                rear_left = -self.speed
                front_right = self.speed
                rear_right = self.speed
            elif self.state == MotorState.RIGHT:
                front_left = self.speed
                rear_left = self.speed
                front_right = -self.speed
                rear_right = -self.speed
            elif self.state == MotorState.STOP:
                front_left = 0
                rear_left = 0
                front_right = 0
                rear_right = 0
        try:
            # Update the database with values from self
            db.insert(MotorsTable.table_name, {
                'id': motor_read_id,
                'front_left': front_left,
                'front_right': front_right,
                'rear_left' : rear_left,
                'rear_right': rear_right,
                'timestamp' : time.time()
            })
            motor_read_id += 1
        except PolyhedraDatabase.UnknownError:
            print "Motor database entry failed."
    return func_wrapper


def database_grid_update(func):

    '''
        After each grid  function call,
        ensure that the grid positions are stored
        in the database.
    '''
    global grid_read_id

    def func_wrapper(self, *args, **kwargs):
        global grid_read_id
        # Call the originating function first,
        # so that the instance fields are up to date.
        result = func(self, *args, **kwargs)

        # Update the database with values from self
        # TODO add iteration id, so each grid is on the same ID
        for cell in self.cells:
            db.insert(GridTable.table_name, {
                'id': grid_read_id,
                'row': cell.x,
                'column': cell.y,
                'lat': cell.lat,
                'lon': cell.lon,
                'cost': cell.cost,
                'heuristic': cell.heuristic,
                'final': cell.final,
                'parent': cell.parent,
                'timestamp': time.timestamp()
            })
            grid_read_id += 1
    return func_wrapper
