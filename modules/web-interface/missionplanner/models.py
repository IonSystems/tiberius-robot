from django.db import models


class Waypoint(models.Model):
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    altitude = models.DecimalField(max_digits=9, decimal_places=6)

class Task(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
'''
    A mission is a collection of MissionAssignments.
'''
class Mission(models.Model):
    tasks = models.ManyToManyField(Task, through='MissionAssignment')
    waypoints = models.ManyToManyField(Waypoint, through='MissionAssignment')
'''
    Assigns waypoints and tasks to missions.
    Each MissionAssignment represensts:
    - a waypoint
    - OR a waypoint and a task
    - OR a task

    This structure can be adapted to suit waypoint defined missions
    or task defined missions.
'''
class MissionAssignment(models.Model):
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE)
    waypoint = models.ForeignKey(Waypoint, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    order = models.IntegerField()
