import falcon
import sys
from tiberius.logger import logger
import logging
from tiberius.control_api.task import *
from tiberius.control_api.tasks.driving_tasks import *

'''
    Controls motor speed, direction, steering angle.
''' 

class TaskControllerResource(object):

    def __init__(self):
            self.logger = logging.getLogger('tiberius.control_api.TaskControllerResource')
            self.tasks = self.find_tasks()
            self.current_task_id = None

    #@falcon.before(validate_params(req, resp, resource, params))
    def on_get(self, req, resp):
        resp.body = '{"status":{"motors": "forward"}}'

    def find_tasks(self):
        tasks = set()
        for task in Task.__subclasses__():
            if task not in tasks:
                tasks.add(task)
	    print task
        return tasks

    def run_task(self, task_id):
	for task in self.tasks:
	    print task
	    if(task.task_id == task_id):
		task.runTask()

def validate_params(req, resp, resource, params):
    if req.content_type not in ALLOWED_IMAGE_TYPES:
        msg = 'Image type not allowed. Must be PNG, JPEG, or GIF'
        raise falcon.HTTPBadRequest('Bad request', msg)


#For debugging purposes
if __name__ == "__main__":
    r = TaskControllerResource()
    print r.find_tasks()
    r.run_task(0)
