import falcon
import sys
from tiberius.logger import logger
import logging
import task

'''
    Controls motor speed, direction, steering angle.
'''
class TaskControllerResource(object):

    def __init__(self):
            self.logger = logging.getLogger('tiberius.control_api.TaskControllerResource')
            self.tasks = find_tasks()
            self.current_task_id = None

    #@falcon.before(validate_params(req, resp, resource, params))
    def on_get(self, req, resp):
        resp.body = '{"status":{"motors": "forward"}}'

    def find_tasks(self, task_id):
        tasks = set()
        parent = Task()
        for task in parent.__subclasses__():
            if child not in tasks:
                tasks.add(child)
        return tasks

    #def run_task(self, task_id)

def validate_params(req, resp, resource, params):
    if req.content_type not in ALLOWED_IMAGE_TYPES:
        msg = 'Image type not allowed. Must be PNG, JPEG, or GIF'
        raise falcon.HTTPBadRequest('Bad request', msg)


#For debugging purposes
if __name__ == "__main__":
    r = TaskControllerResource()
    print r.find_tasks()
