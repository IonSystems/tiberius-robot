from control.control import Control
c = Control()
if __name__ == "__main__":
	try:
		c.driveStraight(50,13) #50% speed for 11.5s
		c.turnRight90Degrees()
		c.driveStraight(50, 15)
		c.turnRight90Degrees()
		
	except KeyboardInterrupt:
		c.motors.stop()
