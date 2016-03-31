import falcon
import sys
from tiberius.logger import logger
import logging


def generate_response(req, resp, resource):
    # If we make it this far then return status OK
    resp.status = falcon.HTTP_200
    resp.body = json.dumps({
                 'connection': 'Online',
                #  'latitude': resource.y,
                #  'longitude': resource.z,
                #  'altitude': resource.state.value,
                #  'speed': resource.speed,
    })


class StatusResource(object):
    '''
        Provides status off Tiberius subsystems.
    '''
    def __init__(self, motor_resource, database_resource, sensor_resource):
        self.logger = logging.getLogger('tiberius.control_api.StatusResource')

    @falcon.after(generate_response)
    def on_post(self, req, resp):
        pass
