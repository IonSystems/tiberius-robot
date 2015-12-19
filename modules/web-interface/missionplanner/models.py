from django.db import models

from django.contrib.auth.models import User

from control.models import TiberiusRobot

class Waypoint(models.Model):
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    altitude = models.DecimalField(max_digits=9, decimal_places=6)

class Task(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=50, null = True)

'''
    A mission is a collection of MissionAssignments.
'''
class Mission(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500, null = True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, default = '0')
    robot = models.ForeignKey(TiberiusRobot, on_delete=models.CASCADE, default = '0')
    #tasks = models.ManyToManyField(Task, through='MissionAssignment')
    #waypoints = models.ManyToManyField(Waypoint, through='MissionAssignment')


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
