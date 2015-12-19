from django.contrib import admin

# Register your models here.

from .models import *
admin.site.register(Mission)
admin.site.register(MissionObjective)
admin.site.register(Task)
admin.site.register(Waypoint)
