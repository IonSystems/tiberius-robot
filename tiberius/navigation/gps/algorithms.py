import math

from tiberius.control.gps20 import GlobalPositioningSystem
from tiberius.utils import bearing_math

if not __debug__:
    from tiberius.control.control import Control


class Algorithms:
    """
    Set of algorithms that control tiberius using the gps and compass.

    Point to point algorithm moves from one longitude and latitude position
    to another. Created

    TODO: Follow path algorithm moves to a location using multiple point to
        point calls to create a path that can move around objects or along a
        given path.
    """

    def __init__(self):
        self.gps = GlobalPositioningSystem()

        if not __debug__:
            self.control = Control()
        self.SPEED = 0.5  # meters/second

        # get the current location of tiberius

    def getLocation(self):
        while self.gps.latitude is None:
            print 'Not valid gps fix, retying...'
            self.gps.update()
        # TESTING REMOVE
        for i in range(0, 10):
            self.gps.update()
        if __debug__:
            self.gps.latitude = 55.912658
            self.gps.longitude = -3.321353
        # -----------------------------
        count = 0
        if count is not 10:
            if self.gps.latitude is "" or self.gps.longitude is "":
                self.gps.update()
        else:
            "No gps values gained"
            return None
        return [self.gps.latitude, self.gps.longitude]

        # get the desired heading for tiberius

    def getHeading(self, curlocation, destination):

        theata1 = math.radians(curlocation[0])
        theata2 = math.radians(destination[0])

        deltaThetha = math.radians(destination[0] - curlocation[0])
        deltaLambda = math.radians(destination[1] - curlocation[1])

        y = math.sin(deltaLambda) * math.cos(theata2)
        x = math.cos(theata1) * math.sin(theata2) - \
            math.sin(theata1) * math.cos(theata2) * math.cos(deltaLambda)
        bearing = math.degrees(math.atan2(y, x)) + 180
        bearing_math.normalize_bearing(bearing)

        return bearing

    def getDistance(self, curlocation, destination):

        r = 6371000.0  # radius of the earth in meters

        theta1 = math.radians(curlocation[0])
        theta2 = math.radians(destination[0])

        deltaTheta = math.radians(destination[0] - curlocation[0])
        deltaLambda = math.radians(destination[1] - curlocation[1])

        a = math.pow(math.sin(deltaTheta / 2.0), 2) + \
            math.cos(theta1) * math.cos(theta2) * \
            math.pow(math.sin(deltaLambda / 2.0), 2)

        c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))

        d = r * c

        return d

    # untested
    def getDestination(self, startlocation, distance, bearing):
        r = 6371000.0
        destination = []
        startlat = math.radians(startlocation[0])
        startlon = math.radians(startlocation[1])

        destination[0] = math.asin(math.sin(startlat) * math.cos(distance / r) +
                                   math.cos(startlat) * math.sin(distance / r) * math.cos(bearing))

        x = math.sin(bearing) * math.sin(distance / r) * math.cos(startlocation[0])
        y = math.cos(distance / r) - math.sin(startlat) * math.sin(destination[0])
        destination[1] = startlon + math.atan2(x, y)

        return destination

    # move from current location to a given destination (a longitude and latitude)
    def pointToPoint(self, destination, speedpercent):

        destination[0] = float(destination[0])
        destination[1] = float(destination[1])

        int(speedpercent)
        checkdistance = 10.0

        speed = 100 / speedpercent

        curlocation = self.getLocation()
        if curlocation is None:
            return
        print 'The current Location is:' + str(curlocation)

        heading = self.getHeading(curlocation, destination)

        distance = self.getDistance(curlocation, destination)

        time = checkdistance / (self.SPEED / speed)

        if not __debug__:
            self.control.turnTo(heading)

        while distance > 1:

            if checkdistance > 0.5:
                if distance < (checkdistance * 2):
                    checkdistance /= 2

            if not __debug__:
                self.control.driveStraight(speedpercent, time)

            # distance -= checkdistance  # this is the next thing that might go wrong

            curlocation = self.getLocation()
            if curlocation is None:
                return

            newheading = self.getHeading(curlocation, destination)

            distance = self.getDistance(curlocation, destination)
            if not (heading + 5 < newheading < 5 - heading):
                heading = newheading
                print '-----------------------------------'
                print 'Current Heading: ' + str(heading)
                print 'Current Location: ' + str(curlocation)
                print 'Destination Location: ' + str(destination)
                print 'Distance Remaining: ' + str(distance)
                print '-----------------------------------'
                print '\r\n'
                distance = self.getDistance(curlocation, destination)
                if not __debug__:
                    self.control.turnTo(heading)

        curlocation = self.getLocation()
        if curlocation is None:
            return
        heading = self.getHeading(curlocation, destination)
        distance = self.getDistance(curlocation, destination)
        time = distance / (self.SPEED / speed)

        if not __debug__:
            self.control.turnTo(heading)
            self.control.driveStraight(speedpercent, time)

        print "The task is complete"
        print "The current location of tiberius is : " + str(curlocation)
        print "With the desired location being : " + str(destination)

    def followPath(self, points, speedpercent):
        for i in range(0, points.__len__(), 1):
            destination = points[i]
            self.pointToPoint(destination, speedpercent)

        print "The task is complete"
        print "The current location of tiberius is : " + str(self.getLocation())
        print "with the desired location being : " + str(destination)
