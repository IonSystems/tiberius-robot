import falcon

import sensors


api = application = falcon.API()

sensors = sensors.SensorResource()
api.add_route('/sensors', sensors)
