# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TiberiusRobot',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('ip_address', models.GenericIPAddressField(protocol=b'IPv4')),
                ('mac_address', models.CharField(max_length=30)),
                ('control_enabled', models.BooleanField()),
                ('autonomy_enabled', models.BooleanField()),
                ('object_detection_enabled', models.BooleanField()),
                ('database_enabled', models.BooleanField()),
                ('image', models.ImageField(upload_to=b'')),
            ],
        ),
    ]
