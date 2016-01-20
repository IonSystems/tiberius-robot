from tiberius.control_api.task import Task

from tiberius.control.control import Control

class DriveForwardsUntilWall(Task):

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
