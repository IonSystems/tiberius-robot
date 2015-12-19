# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('missionplanner', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MissionObjective',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.IntegerField()),
            ],
        ),
        migrations.RemoveField(
            model_name='missionassignment',
            name='mission',
        ),
        migrations.RemoveField(
            model_name='missionassignment',
            name='task',
        ),
        migrations.RemoveField(
            model_name='missionassignment',
            name='waypoint',
        ),
        migrations.RemoveField(
            model_name='mission',
            name='tasks',
        ),
        migrations.RemoveField(
            model_name='mission',
            name='waypoints',
        ),
        migrations.AddField(
            model_name='mission',
            name='creator',
            field=models.ForeignKey(default=b'0', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='mission',
            name='description',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='mission',
            name='name',
            field=models.CharField(default='Name', max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='task',
            name='description',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.DeleteModel(
            name='MissionAssignment',
        ),
        migrations.AddField(
            model_name='missionobjective',
            name='task',
            field=models.ForeignKey(to='missionplanner.Task'),
        ),
        migrations.AddField(
            model_name='missionobjective',
            name='waypoint',
            field=models.ForeignKey(to='missionplanner.Waypoint'),
        ),
        migrations.AddField(
            model_name='mission',
            name='mission_assignment',
            field=models.ForeignKey(default=0, to='missionplanner.MissionObjective'),
            preserve_default=False,
        ),
    ]
