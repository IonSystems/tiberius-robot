from tiberius.database.polyhedra_database import PolyhedraDatabase
from tiberius.database.table_names import TableNames
import time

db = PolyhedraDatabase("decorator_instance")


def database_arm_update(func):
    '''
        After each arm movement function call,
        ensure that the arm positions are stored
        in the database.
    '''
    def func_wrapper(self, change, angle=None):
        # Call the originating function first,
        # so that the instance fields are up to date.
        result = func(self, change, angle=None)

        # Update the database with values from self
        db.insert(TableNames.ARM_TABLE, {
            'id': arm_read_id,
            'X': self.x,
            'Y': self.y,
            'Z' : self.z,
            'waist': self.waist_angle,
            'elbow': self.elbow_angle,
            'shoulder': self.shoulder_angle,
            'timestamp': time.time()
        })
    return func_wrapper
