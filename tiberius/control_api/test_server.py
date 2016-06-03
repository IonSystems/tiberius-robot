import falcon
import sys
from wsgiref import simple_server


# #Import control module

import debug
api = application = falcon.API(media_type='application/json; charset=utf-8')

debug = debug.DebugResource()


api.add_route('/sensors', debug)
api.add_route('/motors', debug)
api.add_route('/arm', debug)
api.add_route('/debug', debug)
api.add_route('/task', debug)
api.add_route('/database', debug)
api.add_route('/status', debug)

if __name__ == '__main__':
    httpd = simple_server.make_server('0.0.0.0', 8001, api)
    httpd.serve_forever()
