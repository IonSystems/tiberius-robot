import falcon
import json
import sys
from enum import Enum
from tiberius.logger import logger
import logging
'''
    Controls motor speed, direction, steering angle.
'''


class RobotArmStates(Enum):
    ENABLED = "enabled"
    DISABLED = "disbled"


def generate_response(req, resp, resource):
    # If we make it this far then return status OK
    resp.status = falcon.HTTP_200
    resp.body = json.dumps({
                 'x': resource.x,
                 'y': resource.y,
                 'z': resource.z,
                 'state': resource.state.value,
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
        self.state = RobotArmStates.ENABLED

        self.x = None
        self.y = None
        self.z = None

    @falcon.after(generate_response)
    @falcon.before(validate_params)
    def on_post(self, req, resp):
        # Can't go forwards and backwards at the same time so we can use elif.
        print req.params
