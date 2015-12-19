# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Mission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='MissionAssignment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.IntegerField()),
                ('mission', models.ForeignKey(to='missionplanner.Mission')),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Waypoint',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('latitude', models.DecimalField(max_digits=9, decimal_places=6)),
                ('longitude', models.DecimalField(max_digits=9, decimal_places=6)),
                ('altitude', models.DecimalField(max_digits=9, decimal_places=6)),
            ],
        ),
        migrations.AddField(
            model_name='missionassignment',
            name='task',
            field=models.ForeignKey(to='missionplanner.Task'),
        ),
        migrations.AddField(
            model_name='missionassignment',
            name='waypoint',
            field=models.ForeignKey(to='missionplanner.Waypoint'),
        ),
        migrations.AddField(
            model_name='mission',
            name='tasks',
            field=models.ManyToManyField(to='missionplanner.Task', through='missionplanner.MissionAssignment'),
        ),
        migrations.AddField(
            model_name='mission',
            name='waypoints',
            field=models.ManyToManyField(to='missionplanner.Waypoint', through='missionplanner.MissionAssignment'),
        ),
    ]
