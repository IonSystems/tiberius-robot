from django.db import models
from django.contrib.auth.models import User

from fleet.models import Robot

import json

class Waypoint(models.Model):
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    altitude = models.DecimalField(max_digits=9, decimal_places=6)

    def __unicode__(self):
        return u'{0}'.format(
            "lat:" + str(self.latitude) + ", "
            "lng:" + str(self.longitude) + ", "
            "alt:" + str(self.altitude)
        )

    def dict(self):
        return {"id": str(self.id),
                "latitude": str(self.latitude),
                "longitude": str(self.longitude),
                "altitude": str(self.altitude)
                }

    def natural_key(self):
        return self.dict()


class Task(models.Model):
    task_id = models.IntegerField()
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=50, null=True)
    estimated_duration = models.CharField(max_length=50, default="Unknown")
    supported_platforms = models.ManyToManyField(
        Robot, related_name="task_supported_platforms")

    def __unicode__(self):
        return u'{0}'.format(
            str(self.name)
        )

    def dict(self):
        return {"id": str(self.task_id),
                "name": str(self.name),
                "description": str(self.description),
                "estimated_duration": str(self.estimated_duration),
                "supported_platforms": str(self.supported_platforms),
                }

    def natural_key(self):
        return self.dict()


class Mission(models.Model):
    '''
        A mission is a collection of MissionAssignments.
    '''
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500, null=True)

    # The creator of the mission
    creator = models.ForeignKey(User, on_delete=models.CASCADE, default='0')

    # The robot the mision is assigned to
    #robot = models.ForeignKey(Robot, on_delete=models.CASCADE, default = '0')
    supported_platforms = models.ManyToManyField(
        Robot, related_name="mission_supported_platforms")

    #estimated_duration = models.DurationField()

    scheduled_start = models.DateTimeField(auto_now=False, auto_now_add=False)

    def __unicode__(self):
        return u'{0}'.format(
            str(self.name)
        )

    def get_absolute_url(self):
        return "/missionplanner/view_mission/%i/" % self.id


class MissionObjective(models.Model):
    '''
        Assigns waypoints and tasks to missions.
        Each MissionObjective represensts:
        - a waypoint
        - OR a waypoint and a task
        - OR a task

        This structure can be adapted to suit waypoint defined missions
        or task defined missions.
    '''
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE)
    waypoint = models.ForeignKey(Waypoint, on_delete=models.CASCADE, null=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, null=True)
    order = models.IntegerField()

    def data_to_class(self, data, mission_id):
        print "lat: " + str(data['latLng']['lat'])
        print "lng: " + str(data['latLng']['lng'])

        print "mission id: " + str(mission_id)

    def __unicode__(self):
        return u'{0}'.format(
            "lat:" + str(self.waypoint.latitude) + ", "
            "lng:" + str(self.waypoint.longitude)
        )
