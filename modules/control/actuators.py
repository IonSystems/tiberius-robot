import md03

class Motor:
	'''
		Tiberius's four motors.
		Contains basic motor movement methods.
		Does not contain any feedback.
	'''
	front_left = md03.MotorDriver(0x58)
	rear_left = md03.MotorDriver(0x5A)
	front_right = md03.MotorDriver(0x5B)
	rear_right = md03.MotorDriver(0x59)
	
	# 0 - 255
	speed = 255
	accel = 0


	def stop(self):
		self.front_left.move(0, self.accel)
		self.rear_left.move(0, self.accel)
		self.front_right.move(0, self.accel)
		self.rear_right.move(0, self.accel)

	def moveForward(self):
		self.front_left.move(self.speed, self.accel)
	        self.rear_left.move(self.speed, self.accel)
        	self.front_right.move(self.speed, self.accel)
   		self.rear_right.move(self.speed, self.accel)

	def moveBackward(self):
		self.front_left.move(-self.speed, self.accel)
		self.rear_left.move(-self.speed, self.accel)
		self.front_right.move(-self.speed, self.accel)
		self.rear_right.move(-self.speed, self.accel)

	#Turn on the spot, to the right
	def turnRight(self):
		self.front_left.move(self.speed, self.accel)
		self.rear_left.move(self.speed, self.accel)
		self.front_right.move(-self.speed, self.accel)
		self.rear_right.move(-self.speed, self.accel)

	#Turn on the spot, to the left
	def turnLeft(self):
		self.front_right.move(-self.speed, self.accel)
		self.rear_leftr.move(-self.speed, self.accel)
		self.front_right.move(self.speed, self.accel)
		self.rear_right.move(self.speed, self.accel)
