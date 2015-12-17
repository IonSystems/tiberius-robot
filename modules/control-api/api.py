import falcon
import sys
from wsgiref import simple_server

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

if __name__ == '__main__':
    httpd = simple_server.make_server('127.0.0.1', 8000, api)
    httpd.serve_forever()
