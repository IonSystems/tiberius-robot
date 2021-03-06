#!/usr/bin/python
import sensors
import actuators
import math
import time
import logging
import tiberius.database.query as db_q
from tiberius.logger import logger
from tiberius.utils import bearing_math
from tiberius.config.config_parser import TiberiusConfigParser
from tiberius.control.exceptions import SensorNotEnabledError
from tiberius.database.tables import CompassTable


"""
.. module:: control
   :synopsis: Provides access to all actuators and sensors supported by Tiberius.
   Contains control loops, using sensor data to control tiberius's actuators.

.. moduleauthor:: Cameron A. Craig <camieac@gmail.com>
"""
c_logger = logging.getLogger('tiberius.control.Control')


class Control:
    """Provides methods to control the motors, via the I2C interface to the motor drivers.

    Uses sensor feedback to accurately manoeuvre the vehicle.
    """

    ultrasonics = sensors.Ultrasonic()
    if TiberiusConfigParser.isCompassEnabled():
        compass = sensors.Compass()

    if TiberiusConfigParser.areMotorsEnabled():
        motors = actuators.Motor()

    if TiberiusConfigParser.isArmEnabled():
        arm = actuators.Arm()

    def __init__(self):
        self.logger = logging.getLogger('tiberius.control.Control')
        self.logger.info('Creating an instance of Control')

    def frontNotHit(self, distance):
        """Determine whether an object has been detected at the front of the vehicle.

        Args:
           distance (str): The theshold distance for detection.
            If the object is closer than distance, then it is classed as a hit.
        """
        fl = self.ultrasonics.senseUltrasonic()['fl'] > distance
        fc = self.ultrasonics.senseUltrasonic()['fc'] > distance
        fr = self.ultrasonics.senseUltrasonic()['fr'] > distance
        if (fl or fc or fr):
            self.logger.debug(
                'Front Right : ' +
                str(fr) +
                ' ,Front Centre: ' +
                str(fc) +
                ' , Front Left: ' +
                str(fl))
        return fl and fc and fr

    def rearNotHit(self, distance):
        """Determine whether an object has been detected at the rear of the vehicle.

        Args:
           distance (int): The theshold distance for detection.
            If the object is closer than distance, then it is classed as a hit.
        """
        rr = self.ultrasonics.senseUltrasonic()['rr'] > distance
        rc = self.ultrasonics.senseUltrasonic()['rc'] > distance
        rl = self.ultrasonics.senseUltrasonic()['rl'] > distance
        if(rr or rc or rl):
            self.logger.debug(
                'Rear Right : ' +
                str(rr) +
                ' ,Rear Centre: ' +
                str(rc) +
                ' , Rear Left: ' +
                str(rl))
        return rr and rc and rl

    def driveForwardUntilWall(self, stop_distance, speed=50):
        """Drive the robot forward until an obstacle is detected.

        Args:
           stop_distance (int): The theshold distance for detection.
            If the object is closer than distance, then it is classed as a hit.
        Kwargs:
           speed (int): The speed percentage of the drive (0 to 100).

        """
        # Wait until Tiberius is stop_distance away from the wall.
        while(self.frontNotHit(stop_distance)):
            self.motors.setSpeedPercent(speed)
            self.motors.moveForward()
        self.motors.stop()

    def driveBackwardUntilWall(self, stop_distance, speed=50):
        """Drive the robot backward until an obstacle is detected.

        Args:
           stop_distance (int): The theshold distance for detection.
            If the object is closer than distance, then it is classed as a hit.
        Kwargs:
           speed (int): The speed percentage of the drive (0 to 100).

        """
        # Wait until Tiberius is 5cm away from the wall.
        while(self.rearNotHit(stop_distance)):
            self.motors.setSpeedPercent(speed)
            self.motors.moveBackward()
        self.motors.stop()

    def turnTo(self, desired_bearing):
        """Turn the robot until it is facing desired_bearing.

        Args:
           desired_bearing (float): The bearing that the robot should be facing
            upon completion of the function.
        """

        # Ensure we have sufficient priviledges to access compass.
        if not TiberiusConfigParser.isCompassEnabled():
            raise SensorNotEnabledError("Compass is disabled, dependant \
function cannot be executed.")

        count = 0
        while(True):
            count += 1
            print 'Iteration: ' + str(count)
            if count < 50:
                time.sleep(0.1)
                # actual_bearing = self.compass.headingNormalized()
                actual_bearing = db_q.get_latest(CompassTable)
                error = actual_bearing - desired_bearing
                # self.logger.debug('Heading: ' + str(actual_bearing))
                # self.logger.debug('Desired: ' + str(desired_bearing))

                if(error < 5 and error > -5):
                    # self.logger.debug('At heading: ' + str(actual_bearing))
                    self.motors.stop()
                    break
                if(error > 180):
                    #print 'error > 180'
                    error -= 360
                if(error < -180):
                    #print 'error < -180'
                    error += 360
                if(error > 0):
                    # print 'error < 0 turning left'
                    self.motors.setSpeedPercent(100)
                    self.motors.turnLeft()

                    # Reduce speed on approach to desired bearing
                    # Positive error is a left turn
                    if(error < 60):
                        self.motors.setSpeedPercent(70)
                        self.motors.turnLeft()
                    if(error < 30):
                        self.motors.setSpeedPercent(40)
                        self.motors.turnLeft()
                    if(error < 5):
                        self.motors.setSpeedPercent(20)
                        self.motors.turnLeft()
                if(error < 0):
                    # print 'error > 0 turning right'
                    self.motors.setSpeedPercent(100)
                    self.motors.turnRight()

                    # Negative error is a right turn
                    if(error > -60):
                        self.motors.setSpeedPercent(70)
                        self.motors.turnRight()
                    if(error > -30):
                        self.motors.setSpeedPercent(40)
                        self.motors.turnRight()
                    if(error > -5):
                        self.motors.setSpeedPercent(20)
                        self.motors.turnRight()

                # print str(error)
            else:
                print '50 Iterations Complete'
                break

    def turnRight90Degrees(self):
        # Ensure we have sufficient priviledges to access compass.
        if not TiberiusConfigParser.isCompassEnabled():
            raise SensorNotEnabledError("Compass is disabled, dependant \
function cannot be executed.")

        old_bearing = self.compass.headingNormalized()

        desired_bearing = (old_bearing + 90)
        if(desired_bearing > 180):
            desired_bearing -= 360

        print desired_bearing
        self.turnTo(desired_bearing)

    def turnLeft90Degrees(self):
        # Ensure we have sufficient priviledges to access compass.
        if not TiberiusConfigParser.isCompassEnabled():
            raise SensorNotEnabledError("Compass is disabled, dependant \
function cannot be executed.")

        old_bearing = self.compass.headingNormalized()

        desired_bearing = (old_bearing - 90)
        if(desired_bearing < -180):
            desired_bearing += 360

        print desired_bearing
        self.turnTo(desired_bearing)

    # def driveForwardDistance(self, distance_metres):

    def driveStraight(self, speed_percent, duration, sensitivity=1):
        # Ensure we have sufficient priviledges to access compass.
        if not TiberiusConfigParser.isCompassEnabled():
            raise SensorNotEnabledError("Compass is disabled, dependant \
function cannot be executed.")

        desired_heading = self.compass.headingNormalized()
        t = 0  # time

        gain = 1440  # proportional Error multiplier

        integral = 0  # Sum of all errors over time
        i_factor = 1  # integral

        d_factor = 1  # derivative
        previous_error = 0
        debug = False
        left_speed = (speed_percent * 255) / 100  # 0-100 -> 0-255
        right_speed = (speed_percent * 255) / 100
        while t < duration:
            actual_heading = self.compass.headingNormalized()

            error_degrees = actual_heading - desired_heading
            error_degrees = bearing_math.normalize_bearing(error_degrees)

            '''if desired_heading > 0:
                if actual_heading > 0:
                    error_degrees = actual_heading - desired_heading
                elif actual_heading < 0:
                    error_degrees = actual_heading + desired_heading
            elif desired_heading < 0:
                if actual_heading > 0:
                    error_degrees = actual_heading + desired_heading
                elif actual_heading < 0:
                    error_degrees = actual_heading - desired_heading
            '''

            # Make error between 1 and -1
            error = error_degrees / float(180.0)
            error *= sensitivity
            integral += error
            derivative = previous_error - error
            previous_error = error
            if error_degrees < 0:  # Turn Right
                r = right_speed - (abs(error) * gain) - \
                    (integral * i_factor) + (derivative * d_factor)

                l = left_speed + (abs(error) * gain) - \
                    (integral * i_factor) + (derivative * d_factor)

                if debug:
                    print 'Turning RIGHT'
            elif error_degrees > 0:  # Turn Left
                r = right_speed + (abs(error) * gain) - \
                    (integral * i_factor) + (derivative * d_factor)

                l = left_speed - (abs(error) * gain) - \
                    (integral * i_factor) + (derivative * d_factor)

                if debug:
                    print 'Turning LEFT'
            else:
                l = left_speed
                r = right_speed
                integral = 0  # Reset integral error when on track
                if debug:
                    print 'Going STRAIGHT'

            if debug:
                print 'Desired Heading (deg): ' + str(desired_heading)
                print 'Actual Heading (deg): ' + str(actual_heading)
                print 'Error (deg): ' + str(error_degrees)
                print 'Error: ' + str(error)
                print 'Max speed   : ' + str(left_speed)
                print 'Left speed  : ' + str(l)
                print 'Right speed : ' + str(r)

                print 'Proportional: ' + str(error * gain)
                print 'Integral    : ' + str(integral * i_factor)
                print 'Derivative  : ' + str(derivative * d_factor)
            self.motors.moveForwardDualSpeed(l, r)
            time.sleep(0.1)
            t += 0.1
        self.motors.stop()
