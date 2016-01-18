from tiberius.control_api.task import Task

from tiberius.control.control import Control

class DriveForwardsUntilWall(Task):
    def runTask(self):
        control.DriveForwardsUntilWall()
        self.completeTask()

    def pauseTask(self):
        control.stop()

    def resumeTask(self):
        self.runTask()

if __name__ == "__main__":
    task = DriveForwardsUntilWall()
    task.runTask()
