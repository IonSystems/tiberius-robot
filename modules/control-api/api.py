import falcon

import sensors
import motors

api = application = falcon.API(media_type='application/json; charset=utf-8')

sensors = sensors.SensorResource()
api.add_route('/sensors', sensors)
api.add_route('/motors', motors)
