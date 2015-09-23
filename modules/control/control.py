#!/usr/bin/python

import md03
import srf08

class Control:
	'''Control the motor drivers'''
	
	#Front Right
	srffr = srf08.UltrasonicRangefinder(0x72)
	#Front Centre
	srffc = srf08.UltrasonicRangefinder(0x71)
	#Front Left
	srffl = srf08.UltrasonicRangefinder(0x70)
	#Rear Right
	srfrr = srf08.UltrasonicRangefinder(0x73)
	#Rear Centre
	srfrc = srf08.UltrasonicRangefinder(0x74)
	#Rear Left
	srfrl = srf08.UltrasonicRangefinder(0x75)
	
	leftf = md03.MotorDriver(0x58)
	leftr = md03.MotorDriver(0x5A)
	rightf = md03.MotorDriver(0x5B)
	rightr = md03.MotorDriver(0x59)

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
