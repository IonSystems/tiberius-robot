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

	def setSpeedPercent(self, speed_percent):
		self.speed = (255 * speed_percent) / 100

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
		self.front_right.move(self.speed, self.accel)
		self.rear_left.move(-self.speed, self.accel)
		self.front_left.move(-self.speed, self.accel)
		self.rear_right.move(self.speed, self.accel)

	#Used for going forward accurately by adjusting left and right speeds.
	def moveForwardDualSpeed(self, left_speed, right_speed):
		left_speed = self.__clipSpeedValue(left_speed)
		right_speed = self.__clipSpeedValue(right_speed)

		self.front_right.move(right_speed, self.accel)
		self.front_left.move(left_speed, self.accel)
		self.rear_right.move(right_speed, self.accel)
		self.rear_left.move(left_speed, self.accel)

	#Used for going forward accurately by adjusting left and right speeds.
	def moveIndependentSpeeds(self, front_left, front_right, rear_left, rear_right):
		front_left = self.__clipSpeedValue(front_left)
		front_right = self.__clipSpeedValue(front_right)
		rear_left = self.__clipSpeedValue(rear_left)
		rear_right = self.__clipSpeedValue(rear_right)

		self.front_left.move(front_left, self.accel)
		self.front_right.move(front_right, self.accel)
		self.rear_left.move(rear_left, self.accel)
		self.rear_right.move(rear_right, self.accel)

	def __clipSpeedValue(self, speed):
		if speed > 255:
			speed = 255
		elif speed < -255:
			speed = -255
		return speed
