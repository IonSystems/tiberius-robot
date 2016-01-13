import falcon
import sys
from wsgiref import simple_server

import sensors
import motors

# #Import control module
from tiberius.control.control import Control
from tiberius.control.actuators import Motor
from tiberius.control_api.middleware import AuthMiddleware
m = Motor()
api = application = falcon.API(media_type='application/json; charset=utf-8')

sensors = sensors.SensorResource()
motors = motors.MotorResource(m)
api.add_route('/sensors', sensors)
api.add_route('/motors', motors)

if __name__ == '__main__':
    httpd = simple_server.make_server('0.0.0.0', 8000, api)
    httpd.serve_forever()
