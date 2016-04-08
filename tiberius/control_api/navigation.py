
import falcon


class NavigationCommands:
    GOTO_WAYPOINT = "goto_waypoint"


class ReturnStates:
    COMPLETE = "complete"
    INCOMPLETE = "incomplete"


def generate_response(req, resp, resource):
    # If we make it this far then return status OK
    if not resp.status == falcon.HTTP_404:
        resp.status = falcon.HTTP_200
    resp.body = json.dumps({
                 'time_taken': "No time at all",
                 'nav_status': "Complete",
    })


class NavigationResource(object):
    '''
        Allows a user to direct Tiberius to a lat/long location.
    '''
    def __init__(self, algorithms):
        self.algorithms = algorithms

    def on_post(self, req, resp):
        if("command" in req.params):
            command = req.params['command']

            if command == NavigationCommands.GOTO_WAYPOINT:
                latitude = float(req.params['latitude'])
                longitude = float(req.params['longitude'])
                # Speed percent (0 - 100)
                speed = int(req.params['speed'])

                self.algorithms.pointToPoint([longitude, latitude], speed)

        else:
            resp.status = falcom.HTTP_404



        resp.body = '{"data": "Hello world!"}'
        resp.status = falcon.HTTP_200
