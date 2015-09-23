#!/usr/bin/python

import md03
import srf08
import sensors
import actuators

class Control:
	'''
		Provides methods to control the motors,
		via the I2C interface to the motor drivers.
		
		Uses sensor feedback to accurately manoeuvre the vehicle.
	'''
	
	ultrasonics = sensors.Ultrasonic()
	compass = sensors.TiltCompensatedCompass()
	motors = actuators.Motor()

	# 0 - 255
	speed = 255
	accel = 0
	
	def stop(self):
		self.leftf.move(0, self.accel)
		self.leftr.move(0, self.accel)
		self.rightf.move(0, self.accel)
		self.rightr.move(0, self.accel)
		
	def moveForward(self):
		self.leftf.move(self.speed, self.accel)
	        self.leftr.move(self.speed, self.accel)
        	self.rightf.move(self.speed, self.accel)
        	self.rightr.move(self.speed, self.accel)

	def moveBackward(self):
		self.leftf.move(-self.speed, self.accel)
		self.leftr.move(-self.speed, self.accel)
		self.rightf.move(-self.speed, self.accel)
		self.rightr.move(-self.speed, self.accel)
		
	#Turn on the spot, to the right
	def turnRight(self):
		self.leftf.move(self.speed, self.accel)
		self.leftr.move(self.speed, self.accel)
		self.rightf.move(-self.speed, self.accel)
		self.rightr.move(-self.speed, self.accel)
		
	#Turn on the spot, to the left
	def turnLeft(self):
		self.leftf.move(-self.speed, self.accel)
		self.leftr.move(-self.speed, self.accel)
		self.rightf.move(self.speed, self.accel)
		self.rightr.move(self.speed, self.accel)
		
	def senseUltrasonic(self):
		#Tell sensors to write data to it's memory
		# TODO: Currently the doranging() method does all sensors, a bit dodgy
		self.srfrr.doranging()
		
		# Read the data from sensor's memory
		fr = self.srffr.getranging()
		fc = self.srffc.getranging()
		fl = self.srffl.getranging()
		rr = self.srfrr.getranging()
		rc = self.srfrc.getranging()
		rl = self.srfrl.getranging()
		
		return {'fl':fl, 'fc':fc , 'fl':fl, 'rl':rl, 'rc':rc , 'rl':rl}


	
