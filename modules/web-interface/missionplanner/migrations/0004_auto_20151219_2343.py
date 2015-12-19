# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('missionplanner', '0003_auto_20151219_2340'),
    ]

    operations = [
        migrations.AlterField(
            model_name='missionobjective',
            name='task',
            field=models.ForeignKey(to='missionplanner.Task', null=True),
        ),
        migrations.AlterField(
            model_name='missionobjective',
            name='waypoint',
            field=models.ForeignKey(to='missionplanner.Waypoint', null=True),
        ),
    ]
