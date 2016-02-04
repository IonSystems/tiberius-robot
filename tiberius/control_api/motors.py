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


def generate_response():
    def hook(req, resp, resource):
        # If we make it this far then return status OK
        resp.status = falcon.HTTP_200
        resp.body = {
                     'speed': resource.speed,
                     'state': resource.state,
        }
    return hook


def validate_params():
    def hook(req, resp, resource, params):
        # Ensure speed value is between 0 and 100
        if 'speed' in req.params:
            if 0 > int(params['speed']):
                params['speed'] = 0

            if 100 < int(params['speed']):
                params['speed'] = 100
    return hook


class MotorResource(object):

    def __init__(self, motor_control):
        self.motor_control = motor_control
        self.logger = logging.getLogger('tiberius.control_api.MotorResource')
        self.speed = 50
        self.state = MotorStates.STOP

    @falcon.before(validate_params())
    def on_post(self, req, resp):
	print str(req.params)
	print MotorStates.FORWARD.value
	print MotorStates.STOP.value
        # Can't go fowards and backwards at the same time so we can use elif.
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

    @falcon.after(generate_response())
    def proc_forward(self):
        self.motor_control.setSpeedPercent(self.speed)
        self.motor_control.moveForward()
        self.logger.debug("Moving forward at speed %s", self.speed)

    @falcon.after(generate_response())
    def proc_backward(self):
        # speed = int(req.params['backward'])
        self.motor_control.setSpeedPercent(self.speed)
        self.motor_control.moveBackward()
        self.logger.debug("Moving backward at speed %s", self.speed)

    @falcon.after(generate_response())
    def proc_left(self):
        self.motor_control.setSpeedPercent(self.speed)
        self.motor_control.turnLeft()
        self.logger.debug("Turning left at speed %s", self.speed)

    @falcon.after(generate_response())
    def proc_right(self):
        self.motor_control.setSpeedPercent(self.speed)
        self.motor_control.turnRight()
        self.logger.debug("Turning right at speed %s", self.speed)

    @falcon.after(generate_response())
    def proc_stop(self):
        self.motor_control.stop()
        self.logger.debug("Stopped")

    @falcon.after(generate_response())
    def proc_speed(self):
        speed = int(req.params['speed'])
        self.logger.debug("Setting speed to %s", self.speed)
