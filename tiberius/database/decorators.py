from tiberius.database.polyhedra_database import PolyhedraDatabase
from tiberius.database.table_names import TableNames
import time

db = PolyhedraDatabase("decorator_instance")
arm_read_id = 0

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
        arm_read_id += 1
    return func_wrapper
