# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-11 09:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fleet', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='robot',
            name='image',
            field=models.ImageField(upload_to=b'robot_images'),
        ),
    ]
