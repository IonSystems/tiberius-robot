
import falcon
from tiberius.database_wrapper.polyhedra_database import PolyhedraDatabase

class DatabaseCommands:
    QUERY = "query"
    INSERT = "insert"
    
class DatabaseResource(object):
    '''
        Allows access to the in-memory database on Tiberius.
    '''
    def __init__(self):
        self.database = PolyhedraDatabase('api_connection')

    def on_post(self, req, resp):

        if DatabaseCommands.QUERY in req.params:
            table = params['table']
            columns = params['columns']
        resp.body = '{"data": "Hello world!"}'
        resp.status = falcon.HTTP_200
