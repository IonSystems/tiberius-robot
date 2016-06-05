import falcon
import sys
import json
from tiberius.logger import logger
import logging
'''
    Controls motor speed, direction, steering angle.
'''


class DebugResource(object):

    def __init__(self):
        self.logger = logging.getLogger('tiberius.control_api.DebugResource')
	self.left_speed = 0
	self.right_speed = 0

    #@falcon.before(validate_params(req, resp, resource, params))
    def on_get(self, req, resp):
        resp.body = '{"status":{"motors": "forward"}}'

    def on_post(self, req, resp):
        print "Received POST"
	for k in req.params:
	    print str(k) + " : " + req.params[k]
            if(k == "right_speed"):
                self.right_speed = req.params[k]
            elif(k == "left_speed"):
                self.left_speed = req.params[k]
	    resp.status = falcon.HTTP_200
	    resp.body = json.dumps({
	        'left_speed': self.left_speed,
	        'right_speed': self.right_speed
            })

