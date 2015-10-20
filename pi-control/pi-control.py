import sys
sys.path.insert(0, '../modules/database/sqlite')
sys.path.insert(0, '../modules/control')
from client import DatabaseClient
from control import Motor

'''
    Starts up all processes required to be running on the control pi. This includes:
    - Diagnostics Thread: Monitors database for unusual behaviour.
    - Motor Control Thread: Monitors database for motor commands.
    - Keyboard Control Thread: Monitors a socket for a UDP connection, for keyboard control.
    - Lighting Control Thread: Monitors database for lighting commands.
'''
class PiControl:
    '''
        Constantly reads from databse
    '''
    def __init__(self):
        self.db = DatabaseClient()

    def motor_monitor(self):
        m = Motor()
        while(True):
            v = self.db.getMotorValues()
            m.moveIndependentSpeeds(v['fl'],v['fr'], v['rl'], v['rr'])

    def lighting_monitor(self):
        return 1
