
import falcon


class NavigationResource(object):
    '''
        Allows a user to direct Tiberius to a lat/long location.
    '''
    def __init__(self, control):
        self.database = PolyhedraDatabase('api_connection')

    def on_post(self, req, resp):
        resp.body = '{"data": "Hello world!"}'
        resp.status = falcon.HTTP_200
