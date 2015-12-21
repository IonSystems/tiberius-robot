from django.db import models

from django.contrib.auth.models import User

from fleet.models import Robot

class Waypoint(models.Model):
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    altitude = models.DecimalField(max_digits=9, decimal_places=6)

class Task(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=50, null = True)
    supported_platforms = models.ManyToManyField(Robot, related_name = "task_supported_platforms")

'''
    A mission is a collection of MissionAssignments.
'''
class Mission(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500, null = True)

    #The creator of the mission
    creator = models.ForeignKey(User, on_delete=models.CASCADE, default = '0')

    #The robot the mision is assigned to
    robot = models.ForeignKey(Robot, on_delete=models.CASCADE, default = '0')
    supported_platforms = models.ManyToManyField(Robot, related_name = "mission_supported_platforms")

    estimated_duration = models.DurationField()

    scheduled_start = models.DateTimeField(auto_now=False, auto_now_add=False)



'''
    Assigns waypoints and tasks to missions.
    Each MissionObjective represensts:
    - a waypoint
    - OR a waypoint and a task
    - OR a task

    This structure can be adapted to suit waypoint defined missions
    or task defined missions.
'''
class MissionObjective(models.Model):
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE)
    waypoint = models.ForeignKey(Waypoint, on_delete=models.CASCADE, null = True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, null = True)
    order = models.IntegerField()
