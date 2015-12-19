# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('missionplanner', '0002_auto_20151219_2336'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mission',
            name='mission_assignment',
        ),
        migrations.AddField(
            model_name='missionobjective',
            name='mission',
            field=models.ForeignKey(default=0, to='missionplanner.Mission'),
            preserve_default=False,
        ),
    ]
