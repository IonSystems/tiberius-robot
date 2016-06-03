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

	def on_post(self, req, resp):
		print "Received POST"
		for k,v in req.params:
			print str(k) + ": " + str(v)
		resp.status = falcon.HTTP_200
		resp.body = json.dumps({
					 'test': "valuetest",
					 'test2': "valuetest"
		})

