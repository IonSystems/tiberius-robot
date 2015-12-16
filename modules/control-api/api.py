import falcon
import sys

import sensors
import motors

# #Import control module
sys.path.insert(0,'../control')
from actuators import Motor
m = Motor()
api = application = falcon.API(media_type='application/json; charset=utf-8')

sensors = sensors.SensorResource()
motors = motors.MotorResource(m)
api.add_route('/sensors', sensors)
api.add_route('/motors', motors)
