
import falcon

#Import motor part of control module
sys.path.insert(0,'../control')
from control import Control.motors as motors

'''
    Controls motor speed, direction, steering angle.
'''
class MotorResource(object):

    def on_get(self, req, resp):
        if(req.size() > 0):
            print req
            if(req == ''):

        resp.body = '{"data": "Hello world!"}'
        resp.status = falcon.HTTP_200
