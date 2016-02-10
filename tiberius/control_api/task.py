import abc
from enum import Enum
from tiberius.control.control import Control


class Task(object):
    '''
    An abstract Task that is implemented in order to build usable tasks for Tiberius to run during a mission.
    '''
    def __init__(self):

        #@abs.abstractproperty
        self.task_name = None
        self.task_id = None
        self.task_description = None

        self.task_complete = self.TaskState.STOPPED

        self.control = Control()

    def __str__(self):
        return str({'name': self.task_name,
                    'task_id': self.task_id})

    def setupTask(self, task_name, task_id, task_description):
        self.task_name = task_name
        self.task_id = task_id
        self.task_description = task_description

    @abc.abstractmethod
    def runTask(self):
        raise NotImplementedError(
            "Task " + self.task_name + "must implement " + __name__)

    @abc.abstractmethod
    def pauseTask(self):
        raise NotImplementedError(
            "Task " + self.task_name + "must implement " + __name__)

    @abc.abstractmethod
    def resumeTask(self):
        raise NotImplementedError(
            "Task " + self.task_name + "must implement " + __name__)

    def completeTask(self):
        self.task_complete = self.TaskState.COMPLETE

    class TaskState(Enum):
        STOPPED = 0
        RUNNING = 1
        PAUSED = 2
        COMPLETE = 3
