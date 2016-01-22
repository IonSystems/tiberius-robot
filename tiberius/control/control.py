#!/usr/bin/python

import md03
import srf08
import sensors
import actuators
import time
import logging

c_logger = logging.getLogger('tiberius.control.Control')


class Control:
    '''
            Provides methods to control the motors,
            via the I2C interface to the motor drivers.

            Uses sensor feedback to accurately manoeuvre the vehicle.
    '''

    ultrasonics = sensors.Ultrasonic()
    compass = sensors.Compass()
    motors = actuators.Motor()

    def __init__(self):
        self.logger = logging.getLogger('tiberius.control.Control')
        self.logger.info('Creating an instance of Control')

    def frontNotHit(self, distance):
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
        # Wait until Tiberius is 5cm away from the wall.
        while(self.frontNotHit(stop_distance)):
            self.motors.setSpeedPercent(speed)
            self.motors.moveForward()
        self.motors.stop()

    def driveBackwardUntilWall(self, stop_distance, speed=50):
        # Wait until Tiberius is 5cm away from the wall.
        while(self.rearNotHit(stop_distance)):
            self.motors.setSpeedPercent(speed)
            self.motors.moveBackward()
        self.motors.stop()

    def turnTo(self, desired_bearing):
        count = 0
        while(True):
            count += 1
            print 'Iteration: ' + str(count)
            if count < 50:
                time.sleep(0.1)
                actual_bearing = self.compass.headingNormalized()
                error = actual_bearing - desired_bearing
                self.logger.debug('Heading: ' + str(actual_bearing))
                self.logger.debug('Desired: ' + str(desired_bearing))

                if(error < 5 and error > -5):
                    self.logger.debug('At heading: ' + str(actual_bearing))
                    self.motors.stop()
                    break
                if(error > 180):
                    print 'error > 180'
                    error -= 360
                if(error < -180):
                    print 'error < -180'
                    error += 360
                if(error > 0):
                    print 'error < 0 turning left'
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
                    print 'error > 0 turning right'
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

                print str(error)
            else:
                print '50 Iterations Complete'
                break

    def turnRight90Degrees(self):
        old_bearing = self.compass.headingNormalized()

        desired_bearing = (old_bearing + 90)
        if(desired_bearing > 180):
            desired_bearing -= 360

        print desired_bearing
        self.turnTo(desired_bearing)

    def turnLeft90Degrees(self):
        old_bearing = self.compass.headingNormalized()

        desired_bearing = (old_bearing - 90)
        if(desired_bearing < -180):
            desired_bearing += 360

        print desired_bearing
        self.turnTo(desired_bearing)

    # def driveForwardDistance(self, distance_metres):

    def driveStraight(self, speed_percent, duration):
        desired_heading = self.compass.headingNormalized()
        t = 0  # time
        gain = 32  # proportional Error multiplier
        integral = 0  # Sum of all errors over time
        i_factor = 8  # integral

        d_factor = 0  # derivative
        previous_error = 0
        debug = True
        left_speed = (speed_percent * 255) / 100  # 0-100 -> 0-255
        right_speed = (speed_percent * 255) / 100
        while(t < duration):
            time.sleep(0.5)
            actual_heading = self.compass.headingNormalized()
            if desired_heading > 0:
                if actual_heading > 0:
                    error_degrees = actual_heading - desired_heading
                elif actual_heading < 0:
                    error_degrees = -((actual_heading + 180) - desired_heading)
            elif desired_heading < 0:
                if actual_heading > 0:
                    error_degrees = actual_heading + desired_heading
                elif actual_heading < 0:
                    error_degrees = actual_heading - desired_heading


            # Make error between 1 and -1
            error = error_degrees / float(360.0)

            integral += error
            derivative = previous_error - error
            previous_error = error
            if error_degrees < 0:  # Turn Right
                r = right_speed - (abs(error) * gain) - (integral * i_factor) + (derivative * d_factor)

                l = left_speed + (abs(error) * gain) - (integral * i_factor) + (derivative * d_factor)

                if debug:
                    print 'Turning RIGHT'
            elif error_degrees > 0:  # Turn Left         
                r = right_speed + (abs(error) * gain) - (integral * i_factor) + (derivative * d_factor)

                l = left_speed - (abs(error) * gain) - (integral * i_factor) + (derivative * d_factor)

                if debug:
                    print 'Turning LEFT'
            else:
                l = left_speed
                r = right_speed
                integral = 0  # Reset integral error when on track
                if debug:
                    print 'Going STRAIGHT'

            if(debug):
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

    def driveStraightStopStart(self, speed_percent, duration):
        desired_bearing = self.compass.headingNormalized()
        t = 0
        self.motors.setSpeedPercent(speed_percent)
        while(t < duration):
            actual_bearing = self.compass.headingNormalized()
            error = actual_bearing - desired_bearing

            if error != 0:
                self.turnTo(desired_bearing)
                self.motors.moveForward()

            else:
                self.motors.moveForward()
            time.sleep(0.1)
            t += 0.1
