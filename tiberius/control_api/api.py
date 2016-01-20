import falcon
import sys
from wsgiref import simple_server

import sensors
import motors
import debug
import task_controller

# #Import control module
from tiberius.control.control import Control
from tiberius.control.actuators import Motor
from tiberius.control_api.middleware import AuthMiddleware

#This is the main instance of Control that is used widely throughout this API.
c = Control()
m = c.motors

api = application = falcon.API(media_type='application/json; charset=utf-8')

sensors = sensors.SensorResource()
motors = motors.MotorResource(m)
debug = debug.DebugResource()
task_controller = task_controller.TaskControllerResource()

api.add_route('/sensors', sensors)
api.add_route('/motors', motors)
api.add_route('/debug', debug)
api.add_route('/task_controller', task_controller)

if __name__ == '__main__':
    httpd = simple_server.make_server('0.0.0.0', 8000, api)
    httpd.serve_forever()
