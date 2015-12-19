# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('control', '0001_initial'),
        ('missionplanner', '0004_auto_20151219_2343'),
    ]

    operations = [
        migrations.AddField(
            model_name='mission',
            name='robot',
            field=models.ForeignKey(default=b'0', to='control.TiberiusRobot'),
        ),
    ]
