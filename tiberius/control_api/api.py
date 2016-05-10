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
from tiberius.config.config_parser import TiberiusConfigParser
from tiberius.control_api.middleware import AuthMiddleware

# This is the main instance of Control that is used widely throughout this API.
c = Control()

api = application = falcon.API(
	media_type='application/json; charset=utf-8',
        #middleware=[AuthMiddleware()]
)

sensors = sensors.SensorResource()
api.add_route('/sensors', sensors)

if TiberiusConfigParser.areMotorsEnabled():
    m = c.motors
    motors = motors.MotorResource(m)
    api.add_route('/motors', motors)

if TiberiusConfigParser.isArmEnabled():
    a = c.arm
    arm = robot_arm.RobotArmResource(a)
    api.add_route('/arm', arm)

debug = debug.DebugResource()
api.add_route('/debug', debug)

task_controller = task_controller.TaskControllerResource()
api.add_route('/task', task_controller)

database = database.DatabaseResource()
api.add_route('/database', database)

status = status.StatusResource(motors, database, sensors)
api.add_route('/status', status)

if TiberiusConfigParser.isGPSEnabled():
    n = Algorithms(c)
    navigation = navigation.NavigationResource(n)
    api.add_route('/navigation', navigation)

if __name__ == '__main__':
    httpd = simple_server.make_server('0.0.0.0', 8000, api)
    httpd.serve_forever()
