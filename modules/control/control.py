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



	
