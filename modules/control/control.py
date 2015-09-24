#!/usr/bin/python

import md03
import srf08
import sensors
import actuators
import time

class Control:
	'''
		Provides methods to control the motors,
		via the I2C interface to the motor drivers.
		
		Uses sensor feedback to accurately manoeuvre the vehicle.
	'''
	
	ultrasonics = sensors.Ultrasonic()
	compass = sensors.Compass()
	motors = actuators.Motor()

	def frontNotHit(self, distance):
		fl = self.ultrasonics.senseUltrasonic()['fl'] > distance
		fc = self.ultrasonics.senseUltrasonic()['fc'] > distance
		fr = self.ultrasonics.senseUltrasonic()['fr'] > distance
		if (fl or fc or fr):
			print 'Front Right : ' + str(fr) + ' ,Front Centre: ' + str(fc) + ' , Front Left: ' + str(fl)
		return fl and fc and fr
	
	def rearNotHit(self, distance):
		rr = self.ultrasonics.senseUltrasonic()['rr'] > distance
		rc = self.ultrasonics.senseUltrasonic()['rc'] > distance
		rl = self.ultrasonics.senseUltrasonic()['rl'] > distance
		if(rr or rc or rl):
			print 'Rear Right : ' + str(rr) + ' ,Rear Centre: ' + str(rc) + ' , Rear Left: ' + str(rl)
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
                        print 'Heading: ' + str(actual_bearing)
                        print 'Desired: ' + str(desired_bearing)
                         
                        if(error < 5 and error > -5):
                                print 'At heading: ' + str(actual_bearing)
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
				self.motors.setSpeed(100)
                                self.motors.turnLeft()

                                #Reduce speed on approach to desired bearing
                                #Positive error is a left turn
                                if(error < 60):
                                        self.motors.setSpeed(70)
                                        self.motors.turnLeft()
                                if(error < 30):
                                        self.motors.setSpeed(40)
                                        self.motors.turnLeft()	
                                if(error < 5):
                                        self.motors.setSpeed(20)
                                        self.motors.turnLeft()
                        if(error < 0):
                                print 'error > 0 turning right'
                                self.motors.setSpeed(100)
				self.motors.turnRight()

                                #Negative error is a right turn
                                if(error > -60):
                                        self.motors.setSpeed(70)
                                        self.motors.turnRight()
                                if(error > -30):
                                        self.motors.setSpeed(40)
                                        self.motors.turnRight()	
                                if(error > -5):
                                        self.motors.setSpeed(20)
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
