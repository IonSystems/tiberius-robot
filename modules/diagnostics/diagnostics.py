import sys
import logging

sys.path.insert(0, '../control')
from control import Control

d_logger = logging.getLogger('tiberius.diagnostics')

class Diagnostics:
	'''
        	Runs constantly during operation of tiberius to look for faults in the system.
	'''
	c = Control()

	def __init__(self):
		self.logger = logging.getLogger('tiberius.diagnostics.Diagnostics')
		self.logger.info('Creating instance of Diagnostics')
	def getMotorCurrent(self):
		fl = self.c.motors.front_left.current()		
		fr = self.c.motors.front_right.current()		
		rl = self.c.motors.rear_left.current()		
		rr = self.c.motors.rear_right.current()
		return {'fl' : fl, 'fr' : fr, 'rl' : rl, 'rr' : rr}
	def getMotorStatus(self):
		fl = self.c.motors.front_left.status()
		fr = self.c.motors.front_right.status()
		rl = self.c.motors.rear_left.status()
		rr = self.c.motors.rear_right.status()
		return {'fl' : fl, 'fr' : fr, 'rl' : rl, 'rr' : rr}

	def isOverCurrent(self, status):
		if ((status >> 1) ^ 1):
			return True
		else:
			return False
if __name__ == "__main__":
	import time

	d = Diagnostics()
	while(True):
		print str(d.getMotorCurrent())
		print str(d.getMotorStatus())
		time.sleep(1)
