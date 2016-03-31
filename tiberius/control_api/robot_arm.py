import falcon
import json
import sys
from enum import Enum
from tiberius.logger import logger
import logging
'''
    Controls motor speed, direction, steering angle.
'''


class ArmStates:
    ENABLED = "enabled"
    DISABLED = "disabled"


class ArmCommands:
    BASKET = "basket"
    CENTRE = "centre"
    PARK = "park"
    SET_X = "set_x"
    SET_Y = "set_y"
    SET_Z = "set_z"
    GRASP = "grasp"
    UNGRASP = "ungrasp"
    SET_SPEED = "set_speed"
    GET_SPEED = "get_speed"


def generate_response(req, resp, resource):
    # If we make it this far then return status OK
    resp.status = falcon.HTTP_200
    resp.body = json.dumps({
                 'x': resource.x,
                 'y': resource.y,
                 'z': resource.z,
                 'state': resource.state.value,
                 'speed': resource.speed,
    })


def validate_params(req, resp, resource):
    # Ensure speed value is between 0 and 100
    params = req.params
    if 'x' in params:
        if 0 > int(params['x']):
            params['x'] = 0
        if 100 < int(params['x']):
            params['x'] = 100

    if 'y' in params:
        if 0 > int(params['y']):
            params['y'] = 0
        if 100 < int(params['y']):
            params['y'] = 100

    if 'z' in params:
        if 0 > int(params['z']):
            params['z'] = 0
        if 100 < int(params['z']):
            params['z'] = 100


class RobotArmResource(object):

    def __init__(self, arm_control):
        self.arm_control = arm_control
        self.logger = logging.getLogger('tiberius.control_api.RobotArmResource')
        self.state = ArmStates.ENABLED

        self.x = None
        self.y = None
        self.z = None

        self.speed = 0

    @falcon.after(generate_response)
    @falcon.before(validate_params)
    def on_post(self, req, resp):
        # Get arm speed
        if(ArmCommands.GET_SPEED in req.params):
            pass
        if(ArmCommands.SET_SPEED in req.params):
            self.speed = req.params[ArmCommands.SET_SPEED]

        # Arm positional commands
        if(ArmCommands.SET_X in req.params):
            self.x = req.params[ArmCommands.SET_X]
        if(ArmCommands.SET_Y in req.params):
            self.y = req.params[ArmCommands.SET_Y]
        if(ArmCommands.SET_Z in req.params):
            self.y = req.params[ArmCommands.SET_Z]

        # Arm gripper commands
        if(ArmCommands.GRASP in req.params):
            self.arm_control.grasp()
        elif(ArmCommands.UNGRASP in req.params):
            self.arm_control.ungrasp()

        # Arm complex commands
        if(ArmCommands.BASKET in req.params):
            self.arm_control.basket()
        elif(ArmCommands.CENTRE in req.params):
            self.arm_control.centre()
        elif(ArmCommands.PARK in req.params):
            self.arm_control.park()

        print req.params
