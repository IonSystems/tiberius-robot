import falcon
import sys
from tiberius.logger import logger
import logging
'''
    Controls motor speed, direction, steering angle.
'''


class DebugResource(object):

    def __init__(self):
        self.logger = logging.getLogger('tiberius.control_api.DebugResource')

    #@falcon.before(validate_params(req, resp, resource, params))
    def on_get(self, req, resp):
        resp.body = '{"status":{"motors": "forward"}}'


def validate_params(req, resp, resource, params):
    if req.content_type not in ALLOWED_IMAGE_TYPES:
        msg = 'Image type not allowed. Must be PNG, JPEG, or GIF'
        raise falcon.HTTPBadRequest('Bad request', msg)
