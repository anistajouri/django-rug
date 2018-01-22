# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-01-21 09:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapi', '0007_auto_20180118_2129'),
    ]

    operations = [
        migrations.RenameField(
            model_name='alertrug',
            old_name='is_active_first_pass',
            new_name='active_audio',
        ),
        migrations.RenameField(
            model_name='alertrug',
            old_name='is_active_second_pass',
            new_name='active_camera',
        ),
        migrations.RenameField(
            model_name='alertrug',
            old_name='is_playback_active',
            new_name='active_light',
        ),
        migrations.AddField(
            model_name='alertrug',
            name='alert_message',
            field=models.BooleanField(default=False),
        ),
    ]