import abc
from enum import Enum

class Task:
    '''
    An abstract Task that is implemented in order to build usable tasks for Tiberius to run during a mission.
    '''
    @abc.abstractmethod
    def __init__(self, task_name, task_id, task_description = None):
        self.task_name = task_name
        self.task_id = task_id
        self.task_description = task_description

        self.task_complete = TaskState.STOPPED

    @abc.abstractmethod
    def runTask(self):
        raise NotImplementedError("Task " + self.task_name + "must implement " + __name__)

    @abc.abstractmethod
    def pauseTask(self):
        raise NotImplementedError("Task " + self.task_name + "must implement " + __name__)

    @abc.abstractmethod
    def resumeTask(self):
        raise NotImplementedError("Task " + self.task_name + "must implement " + __name__)

    def completeTask(self):
        self.task_complete = TaskState.COMPLETE

    class TaskState(Enum):
        STOPPED = 0
        RUNNING = 1
        PAUSED = 2
        COMPLETE = 3
