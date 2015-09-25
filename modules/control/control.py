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
