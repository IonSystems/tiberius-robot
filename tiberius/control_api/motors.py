import falcon
import sys
from enum import Enum
from tiberius.logger import logger
import logging
'''
    Controls motor speed, direction, steering angle.
'''


class MotorStates(Enum):
    FORWARD = "forward"
    BACKWARD = "backward"
    LEFT = "left"
    RIGHT = "right"
    STOP = "stop"


def generate_response(req, resp, resource):
    # If we make it this far then return status OK
    resp.status = falcon.HTTP_200
    resp.body = {
                 'speed': resource.speed,
                 'state': resource.state,
    }


def validate_params(req, resp, resource):
    # Ensure speed value is between 0 and 100
    if 'speed' in req.params:
        if 0 > int(params['speed']):
            params['speed'] = 0

        if 100 < int(params['speed']):
            params['speed'] = 100


class MotorResource(object):

    def __init__(self, motor_control):
        self.motor_control = motor_control
        self.logger = logging.getLogger('tiberius.control_api.MotorResource')
        self.speed = 50
        self.state = MotorStates.STOP

    @falcon.after(generate_response)
    @falcon.before(validate_params)
    def on_post(self, req, resp):
        # Can't go forwards and backwards at the same time so we can use elif.
        if(MotorStates.FORWARD.value in req.params):
            self.proc_forward()
        elif(MotorStates.BACKWARD.value in req.params):
            self.proc_backward()

        # Can't go left and right at the same time so elif.
        if(MotorStates.LEFT.value in req.params):
            self.proc_left()
        elif(MotorStates.RIGHT.value in req.params):
            self.proc_right()

        # Change the set speed of the motors.
        if('speed' in req.params):
            self.proc_speed()

        # Keep STOP at the bottom so nothing can overwrite it!
        if(MotorStates.STOP.value in req.params):
            self.proc_stop()

    def proc_forward(self):
        self.motor_control.setSpeedPercent(self.speed)
        self.motor_control.moveForward()
        self.state = MotorStates.FORWARD
        self.logger.debug("Moving forward at speed %s", self.speed)

    def proc_backward(self):
        # speed = int(req.params['backward'])
        self.motor_control.setSpeedPercent(self.speed)
        self.motor_control.moveBackward()
        self.state = MotorStates.BACKWARD
	self.logger.debug("Moving backward at speed %s", self.speed)

    def proc_left(self):
        self.motor_control.setSpeedPercent(self.speed)
        self.motor_control.turnLeft()
        self.state = MotorStates.LEFT
        self.logger.debug("Turning left at speed %s", self.speed)

    def proc_right(self):
        self.motor_control.setSpeedPercent(self.speed)
        self.motor_control.turnRight()
        self.state = MotorStates.RIGHT
        self.logger.debug("Turning right at speed %s", self.speed)

    def proc_stop(self):
        self.motor_control.stop()
        self.state = MotorStates.STOP
        self.logger.debug("Stopped")

    def proc_speed(self):
        speed = int(req.params['speed'])
        self.logger.debug("Setting speed to %s", self.speed)
        # Now that the speed has been updated,
        # reinitiate any active states.
        if self.state == MotorStates.FORWARD:
            self.proc_forward()
        elif self.state == MotorStates.BACKWARD:
            self.proc_backward()
        elif self.state == MotorStates.LEFT:
            self.proc_left()
        elif self.state == MotorStates.RIGHT:
            self.proc_right()
