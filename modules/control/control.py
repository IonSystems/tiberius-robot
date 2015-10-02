#!/usr/bin/python

import md03
import srf08
import sensors
import actuators
import time
import logging

c_logger = logging.getLogger('tiberius.control')

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
			self.logger.debug('Front Right : ' + str(fr) + ' ,Front Centre: ' + str(fc) + ' , Front Left: ' + str(fl))
		return fl and fc and fr
	
	def rearNotHit(self, distance):
		rr = self.ultrasonics.senseUltrasonic()['rr'] > distance
		rc = self.ultrasonics.senseUltrasonic()['rc'] > distance
		rl = self.ultrasonics.senseUltrasonic()['rl'] > distance
		if(rr or rc or rl):
			self.logger.debug('Rear Right : ' + str(rr) + ' ,Rear Centre: ' + str(rc) + ' , Rear Left: ' + str(rl))
		return rr and rc and rl

        def driveForwardUntilWall(self, stop_distance, speed = 50):
		#Wait until Tiberius is 5cm away from the wall.
		while(self.frontNotHit(stop_distance)):
			self.motors.moveForward(speed)
		self.motors.stop()

        def driveBackwardUntilWall(self, stop_distance, speed = 50):
		#Wait until Tiberius is 5cm away from the wall.
		while(self.rearNotHit(stop_distance)):
			self.motors.moveBackward(speed)
		self.motors.stop()

        def turnTo(self, desired_bearing):
                while(True):
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

                                #Reduce speed on approach to desired bearing
                                #Positive error is a left turn
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

                                #Negative error is a right turn
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

	#def driveForwardDistance(self, distance_metres):
                
	def driveStraight(self, speed_percent, duration):
		desired_heading = self.compass.headingNormalized()
                t = 0
		p_factor = 400 #Error multiplier
		integral = 0 #Sum of all errors over time
		i_factor = 100 
		derivative = 0 #last error - current error
		d_factor = 100
		previous_error = 0
		debug = True
		left_speed = (speed_percent * 255) / 100
		right_speed = (speed_percent * 255) / 100
		while(t < duration):
			actual_heading = self.compass.headingNormalized()
			error = actual_heading - desired_heading
			if debug:
				print 'Error (deg): ' + str(error)
			#Make error between 1 and -1
			error = error / float(360.0)
			integral += error
			derivative = previous_error - error
			previous_error = error
			if error < 0:
				r =  right_speed - (abs(error) * p_factor) - (integral * i_factor) + (derivative * d_factor)
				#((1 - abs(error)) + 1) / 2  * right_speed
				l = left_speed# + (abs(error) * p_factor) + (integral * i_factor) + (derivative * d_factor)
				if debug:
					print 'Turning RIGHT'
			elif error > 0:
				l = left_speed - (abs(error) * p_factor) - (integral * i_factor) + (derivative * d_factor)
				#((1 - abs(error)) + 1) / 2 * left_speed
				r = right_speed# + (abs(error) * p_factor) + (integral * i_factor) + (derivative * d_factor)
				if debug:
					print 'Turning LEFT'
			else:
				l = left_speed
				r = right_speed
				integral = 0 #Reset integral error when on track
				if debug:
					print 'Going STRAIGHT'
			if(debug):
				print 'Max speed   : ' + str(left_speed)
				print 'Left speed  : ' + str(l)
				print 'Right speed : ' + str(r)

				print 'Proportional: ' + str(error * p_factor)
				print 'Integral    : ' + str(integral * i_factor)
				print 'Derivative  : ' + str(derivative * d_factor)
			self.motors.moveForwardDualSpeed(l,r)
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
