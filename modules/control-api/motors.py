import falcon
import sys

'''
    Controls motor speed, direction, steering angle.
'''
class MotorResource(object):
    def __init__(self, motor_control):
            self.motor_control = motor_control

    #@falcon.before(validate_params(req, resp, resource, params))
    def on_get(self, req, resp):

        #Basic commands used for manual control
        if('forward' in req.params):
            speed = req.params['forward']
            self.motor_control.setSpeedPercent(speed)
            self.motor_control.moveForward()
            resp.body = '{"status":{"motors": "forward"}}'
        elif('backward' in req.params):
            speed = req.params['backward']
            self.motor_control.setSpeedPercent(speed)
            self.motor_control.moveForward()
            resp.body = '{"status":{"motors": "backward"}}'
        if('left' in req.params):
            speed = req.params['left']
            self.motor_control.setSpeedPercent(speed)
            motor_control.turnLeft()
            resp.body = '{"status":{"motors": "left"}}'
        elif('right' in req.params):
            speed = req.params['right']
            self.motor_control.setSpeedPercent(speed)
            self.motor_control.turnRight()
            resp.body = '{"status":{"motors": "right"}}'
        if('stop' in req.params):
            self.motor_control.stop()
            resp.body = '{"status":{"motors": "stop"}}'

        resp.status = falcon.HTTP_200

def validate_params(req, resp, resource, params):
    if req.content_type not in ALLOWED_IMAGE_TYPES:
        msg = 'Image type not allowed. Must be PNG, JPEG, or GIF'
        raise falcon.HTTPBadRequest('Bad request', msg)
