# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-01-07 10:18
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapi', '0002_auto_20180107_1018'),
    ]

    operations = [
        migrations.RenameField(
            model_name='alarmclock',
            old_name='auto_stop_minutes',
            new_name='auto_stop_seconds',
        ),
        migrations.RenameField(
            model_name='alarmclock',
            old_name='stop_minutes',
            new_name='stop_seconds_hit_rug',
        ),
        migrations.RenameField(
            model_name='rugalert',
            old_name='auto_stop_minutes',
            new_name='auto_stop_seconds',
        ),
        migrations.RenameField(
            model_name='rugalert',
            old_name='stop_minutes',
            new_name='stop_seconds_hit_rug',
        ),
    ]
