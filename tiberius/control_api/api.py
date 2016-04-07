import falcon
import sys
from wsgiref import simple_server

import sensors
import motors
import robot_arm
import debug
import task_controller
import database
import status
import navigation

# Import control module
from tiberius.control.control import Control
from tiberius.navigation.gps.algorithms import Algorithms
from tiberius.control_api.middleware import AuthMiddleware

# This is the main instance of Control that is used widely throughout this API.
c = Control()
m = c.motors
a = c.arm
n = Algorithms(c)

api = application = falcon.API(media_type='application/json; charset=utf-8',
                               middleware=[AuthMiddleware()])

sensors = sensors.SensorResource()
motors = motors.MotorResource(m)
arm = robot_arm.RobotArmResource(a)
debug = debug.DebugResource()
task_controller = task_controller.TaskControllerResource()
database = database.DatabaseResource()
status = status.StatusResource(motors, database, sensors)
navigation = navigation.NavigationResource(m, n)
api.add_route('/sensors', sensors)
api.add_route('/motors', motors)
api.add_route('/arm', arm)
api.add_route('/debug', debug)
api.add_route('/task', task_controller)
api.add_route('/database', database)
api.add_route('/status', status)
api.add_route('/navigation', navigation)

if __name__ == '__main__':
    httpd = simple_server.make_server('0.0.0.0', 8000, api)
    httpd.serve_forever()
