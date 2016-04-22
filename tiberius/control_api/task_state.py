from enum import Enum


class TaskState(Enum):
    STOPPED = 0
    RUNNING = 1
    PAUSED = 2
    COMPLETE = 3
