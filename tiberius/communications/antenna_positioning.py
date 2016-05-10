import math

import tiberius.database.query as db_q
from tiberius.database.tables import CompassTable, GPSTable
from tiberius.utils import bearing_math
from tiberius.navigation.gps.algorithms import Algorithms

class Antenna:

    def __init__(self, control):
        self.station = [55.912658, -3.321353]
        self.control = control
        self.gps = Algorithms(self.control)
        self.curheading = self.getCurHeading()

    def correct_heading(self):
        curlocation = self.gps.getLocation()
        heading = self.gps.getHeading(curlocation, self.station)

        moveby = heading - self.curheading
        bearing_math.normalize_bearing(moveby)

        if moveby < 0:
            self.moveServo(moveby, 1)  # anti-clockwise
        else:
            self.moveServo(moveby, 0)  # clockwise
        #move servo
        self.curheading = heading

    def moveServo(self, heading, direction):
        if direction == 1:
            a = 1
        else:
            a = 2

    def getCurHeading(self):

        heading = db_q.get_latest(CompassTable) - 90
        return bearing_math.normalize_bearing(heading)