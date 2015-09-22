
class Motor:
	'''
		Tiberius's four motors.
		Contains basic motor movement methods.
		Does not contain any feedback.
	'''
	front_left = md03.MotorDriver(0x58)
	back_left = md03.MotorDriver(0x5A)
	front_right = md03.MotorDriver(0x5B)
	back_right = md03.MotorDriver(0x59)
	
	# 0 - 255
	speed = 255
	accel = 0


	def stop(self):
		self.leftf.move(0, self.accel)
		self.leftr.move(0, self.accel)
		self.rightf.move(0, self.accel)
		self.rightr.move(0, self.accel)

	def moveForward(self):
		self.leftf.move(-self.speed, self.accel)
        self.leftr.move(-self.speed, self.accel)
        self.rightf.move(-self.speed, self.accel)
        self.rightr.move(-self.speed, self.accel)

	def moveBackward(self):
		self.leftf.move(self.speed, self.accel)
		self.leftr.move(self.speed, self.accel)
		self.rightf.move(self.speed, self.accel)
		self.rightr.move(self.speed, self.accel)

	#Turn on the spot, to the right
	def turnRight(self):
		self.leftf.move(-self.speed, self.accel)
		self.leftr.move(-self.speed, self.accel)
		self.rightf.move(self.speed, self.accel)
		self.rightr.move(self.speed, self.accel)

	#Turn on the spot, to the left
	def turnLeft(self):
		self.leftf.move(self.speed, self.accel)
		self.leftr.move(speed, self.accel)
		self.rightf.move(-self.speed, self.accel)
		self.rightr.move(-self.speed, self.accel)
