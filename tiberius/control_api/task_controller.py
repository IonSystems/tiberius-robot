import falcon
import sys
from tiberius.logger import logger
import logging
from tiberius.control_api.task import *
from tiberius.control_api.tasks.driving_tasks import *
import threading
import json

class TaskThread (threading.Thread):
    def __init__(self, threadID, task):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.task = task

    def run(self):
        while not self.task.is_complete:
            self.task.one_iteration()
        self.task.runTask()


def generate_response(req, resp, resource):
    # If we make it this far then return status OK
    if not resp.status == falcon.HTTP_404:
        resp.status = falcon.HTTP_200
    resp.body = json.dumps({
                 'time_taken': "No time at all",
                 'task_status': "Complete",
    })


class TaskControllerResource(object):

    def __init__(self):
        self.logger = logging.getLogger(
            'tiberius.control_api.TaskControllerResource')

        # Find all the tasks avaibale and make them accessible here.
        self.tasks = self.find_tasks()
        self.current_task_id = None

    @falcon.after(generate_response)
    def on_post(self, req, resp):
        print str(req.params)
        command = None
        if("command" in req.params):
            command = req.params['command']

        task_id = None
        if("task_id" in req.params):
            task_id = int(req.params['task_id'])

        task_id = None
        if("available" in req.params):
            resp.status = falcon.HTTP_200
            resp.body = json.dumps(self.tasks)


        if (command is not None) and (task_id is not None):
            if (command == "run") and (self.current_task_id is None):
                if not self.run_task(task_id):
                    resp.status = falcon.HTTP_404

    def find_tasks(self):
        return [cls() for cls in Task.__subclasses__()]

    def run_task(self, task_id):
        task_found = False
        for task in self.tasks:
            if task.task_id == task_id:
		task_found = True
                self.current_task_id = task_id
                self.logger.info("Running Task: %s", str(task))

                # Create a thread to run the task
                task_thread = TaskThread(task_id, task)

                # Start running the task thread
                task_thread.start()

                # Wait for the thread to COMPLETE
                task_thread.join()

                # Set current task back to None
                self.current_task_id = None
            if not task_found:
		return False
            else:
                return True
            # if(task.__class__.task_id == task_id):
            #    task.runTask()


def validate_params(req, resp, resource, params):
    if req.content_type not in ALLOWED_IMAGE_TYPES:
        msg = 'Image type not allowed. Must be PNG, JPEG, or GIF'
        raise falcon.HTTPBadRequest('Bad request', msg)


# For debugging purposes
if __name__ == "__main__":
    r = TaskControllerResource()
    r.run_task(0)
