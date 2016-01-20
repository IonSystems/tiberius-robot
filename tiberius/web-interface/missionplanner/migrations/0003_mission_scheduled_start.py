# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-21 00:54
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('missionplanner', '0002_mission_supported_platforms'),
    ]

    operations = [
        migrations.AddField(
            model_name='mission',
            name='scheduled_start',
            field=models.DateTimeField(default=datetime.datetime(
                2015, 12, 21, 0, 54, 52, 157863, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
