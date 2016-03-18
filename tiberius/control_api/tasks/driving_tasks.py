from tiberius.control_api.task import Task

from tiberius.control.control import Control


class DriveForwardsUntilWall(Task):

    def __init__(self):
        super(DriveForwardsUntilWall, self).__init__()
        self.task_name = 'Drive Forwards Until Wall'
        self.task_id = 0
        self.task_description = '''Drive forwards at half speed until a wall
				is sensed using the ultrasonics with a
				distance of 10cm.'''

    def runTask(self):
        self.control.driveForwardUntilWall(50)
        self.completeTask()

    def pauseTask(self):
        self.control.stop()

    def resumeTask(self):
        self.runTask()

if __name__ == "__main__":
    task = DriveForwardsUntilWall("Drive until wall", 0)
    task.runTask()


class DriveBackwardsUntilWall(Task):

    def __init__(self):
        super(DriveBackwardsUntilWall, self).__init__()
        self.task_name = 'Drive Backwards Until Wall'
        self.task_id = 1
        self.task_description = '''Drive backwards at half speed until a wall
				is sensed using the ultrasonics with a
				distance of 10cm.'''

    def runTask(self):
        self.control.driveBackwardUntilWall(50)
        self.completeTask()

    def pauseTask(self):
        self.control.stop()

    def resumeTask(self):
        self.runTask()

if __name__ == "__main__":
    task = DriveForwardsUntilWall("Drive until wall", 0)
    task.runTask()
