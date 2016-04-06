import md03
from robotic_arm.ramps import RoboticArmDriver
from tiberius.config.config_parser import TiberiusConfigParser
import enum
import time
"""
.. module:: actuators
   :synopsis: Provides access to all actuators supported by Tiberius.
   This most importantly includes the motors to drive Tiberius's wheels.

.. moduleauthor:: Cameron A. Craig <camieac@gmail.com>


"""


class Arm:
    arm = RoboticArmDriver()

    # Store current posisions of each joints
    waist_angle = 0
    shoulder_angle = 0
    elbow_angle = 0


    # Store cartesian coordinates
    x = 0
    y = 0
    z = 0

    #get the points location
    def get_waist(self):
        return self.waist_angle

    def get_shoulder(self):
        return self.shoulder_angle

    def get_elbow(self):
        return self.elbow_angle

    #move the joints
    def rotate_waist(self, change, angle=None):
        if angle:
            self.waist_angle = angle
        else:
            self.waist_angle += change      #move from current location by change
            if self.waist_angle > 360:      #normalize the angle
                self.waist_angle = 360
            elif self.waist_angle < 0:
                self.waist_angle = 0
	print str(self.waist_angle)
        self.arm.move_waist(self.waist_angle)
        time.sleep(0.05)

    def move_shoulder(self, change, angle=None):
        if angle:
            self.shoulder_angle = angle
        else:
            self.shoulder_angle += change
            if self.shoulder_angle > 360:      #normalize the angle
                self.shoulder_angle = 360
            elif self.shoulder_angle < 0:
                self.shoulder_angle = 0
	print str(self.shoulder_angle)
        self.arm.move_shoulder(self.shoulder_angle)
        time.sleep(0.8)

    def move_elbow(self, change, angle=None):
        if angle:
            self.elbow_angle = angle
        else:
            self.elbow_angle += change
            if self.elbow_angle > 360:     #normalize the angle
                self.elbow_angle = 360
            elif self.elbow_angle < 0 :
                self.elbow_angle = 0
	print str(self.elbow_angle)
        self.arm.move_elbow(self.elbow_angle)
        time.sleep(0.05)

class MotorState(enum.Enum):
    STOP = 0
    FORWARD = 1
    BACKWARD = 2
    RIGHT = 3
    LEFT = 4


class Motor:
    '''
            Tiberius's four motors.
            Contains basic motor movement methods.
            Does not contain any feedback.
    '''
    __config = TiberiusConfigParser()

    front_left = md03.MotorDriver(__config.getMotorFrontLeftAddress())
    rear_left = md03.MotorDriver(__config.getMotorRearLeftAddress())
    front_right = md03.MotorDriver(__config.getMotorFrontRightAddress())
    rear_right = md03.MotorDriver(__config.getMotorRearRightAddress())

    state = MotorState.STOP

    # 0 - 255
    speed = 255
    accel = 0

    def setSpeedPercent(self, speed_percent):
        self.speed = (255 * speed_percent) / 100

    def stop(self):
        self.front_left.move(0, 0)
        self.rear_left.move(0, 0)
        self.front_right.move(0, 0)
        self.rear_right.move(0, 0)
        self.state = MotorState.STOP

    def moveForward(self):
        self.front_left.move(self.speed, self.accel)
        self.rear_left.move(self.speed, self.accel)
        self.front_right.move(self.speed, self.accel)
        self.rear_right.move(self.speed, self.accel)
        self.state = MotorState.FORWARD

    def moveBackward(self):
        self.front_left.move(-self.speed, self.accel)
        self.rear_left.move(-self.speed, self.accel)
        self.front_right.move(-self.speed, self.accel)
        self.rear_right.move(-self.speed, self.accel)
        self.state = MotorState.BACKWARD

    # Turn on the spot, to the right
    def turnRight(self):
        self.front_left.move(self.speed, self.accel)
        self.rear_left.move(self.speed, self.accel)
        self.front_right.move(-self.speed, self.accel)
        self.rear_right.move(-self.speed, self.accel)
        self.state = MotorState.RIGHT

    # Turn on the spot, to the left
    def turnLeft(self):
        self.front_right.move(self.speed, self.accel)
        self.rear_left.move(-self.speed, self.accel)
        self.front_left.move(-self.speed, self.accel)
        self.rear_right.move(self.speed, self.accel)
        self.state = MotorState.LEFT

    # Used for going forward accurately by adjusting left and right speeds.
    def moveForwardDualSpeed(self, left_speed, right_speed):
        left_speed = self.__clipSpeedValue(left_speed)
        right_speed = self.__clipSpeedValue(right_speed)

        self.front_right.move(right_speed, self.accel)
        self.front_left.move(left_speed, self.accel)
        self.rear_right.move(right_speed, self.accel)
        self.rear_left.move(left_speed, self.accel)

        # TODO:This is unsafe! could be going forwards,backwards,left or right
        self.state = MotorState.FORWARD

    # Used for going forward accurately by adjusting left and right speeds.
    def moveIndependentSpeeds(
            self,
            front_left,
            front_right,
            rear_left,
            rear_right):
        front_left = self.__clipSpeedValue(front_left)
        front_right = self.__clipSpeedValue(front_right)
        rear_left = self.__clipSpeedValue(rear_left)
        rear_right = self.__clipSpeedValue(rear_right)

        self.front_left.move(front_left, self.accel)
        self.front_right.move(front_right, self.accel)
        self.rear_left.move(rear_left, self.accel)
        self.rear_right.move(rear_right, self.accel)

        # TODO: This is unsafe! could be going forwards,backwards,left or right
        self.state = MotorState.FORWARD

    def __clipSpeedValue(self, speed):
        if speed > 255:
            speed = 255
        elif speed < -255:
            speed = -255
        return speed
