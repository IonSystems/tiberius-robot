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
    HOME = "home"
    CHANGE_X = "arm_dx" # Waist
    CHANGE_Y = "arm_dy" # Shoulder
    CHANGE_Z = "arm_dz" # Elbow
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
                 'state': resource.state,
                 'speed': resource.speed,
    })


def validate_params(req, resp, resource, params):
    # Ensure speed value is between 0 and 100
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

        self.x = -1
        self.y = -1
        self.z = -1

        self.speed = 0

    @falcon.after(generate_response)
    @falcon.before(validate_params)
    def on_post(self, req, resp):
        # Get arm speed
        if(ArmCommands.GET_SPEED in req.params):
            pass
        if(ArmCommands.SET_SPEED in req.params):
            self.speed = req.params[ArmCommands.SET_SPEED]

        if 'command_name' in req.params and 'command_value' in req.params:
            command_name = req.params['command_name']
            command_value = int(req.params['command_value'])
            # Arm positional commands
            if(ArmCommands.CHANGE_X in command_name):
                self.x += command_value
                self.arm_control.move_x(command_value)
            if(ArmCommands.CHANGE_Y in command_name):
                self.y += command_value
                self.arm_control.move_y(command_value)
            if(ArmCommands.CHANGE_Z in command_name):
                self.z += command_value
                self.arm_control.move_z(command_value)

            # Arm gripper commands
            if(ArmCommands.GRASP in command_name):
                self.logger.info("Grasping")
                self.arm_control.close_gripper()
            elif(ArmCommands.UNGRASP in command_name):
                self.logger.info("Ungrasp")
                self.arm_control.open_gripper()

            # Arm complex commands
            # if(ArmCommands.BASKET in req.params):
            #     self.arm_control.basket()
            if(ArmCommands.CENTRE in command_name):
                self.logger.info("Centring")
                self.arm_control.centre()
            elif(ArmCommands.PARK in command_name):
                self.logger.info("Parking")
                self.arm_control.park()
            elif(ArmCommands.HOME in command_name):
                self.logger.info("Homing")
                self.arm_control.home()

            print req.params
