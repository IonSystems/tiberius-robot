
import falcon
'''
    Provides sensor data.
'''


class SensorResource(object):

    def on_get(self, req, resp):
        resp.body = '{"data": "Hello world!"}'
        resp.status = falcon.HTTP_200
