# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-01-08 11:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webapi', '0004_auto_20180107_1650'),
    ]

    operations = [
        migrations.CreateModel(
            name='AlertRug',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('is_active_first_pass', models.BooleanField(default=False)),
                ('is_active_second_pass', models.BooleanField(default=False)),
                ('is_playback_active', models.BooleanField(default=False)),
                ('alert_duration_Seconds', models.IntegerField()),
                ('auto_stop_seconds', models.IntegerField(default=0)),
                ('stop_seconds_hit_rug', models.IntegerField(default=0)),
                ('alarm_clock', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webapi.AlarmClock')),
                ('mp3_playback', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webapi.MP3Playback')),
            ],
        ),
        migrations.RemoveField(
            model_name='rugalert',
            name='alarm_clock',
        ),
        migrations.RemoveField(
            model_name='rugalert',
            name='mp3_playback',
        ),
        migrations.AlterField(
            model_name='alertnotified',
            name='alert_rug',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webapi.AlertRug'),
        ),
        migrations.DeleteModel(
            name='RugAlert',
        ),
    ]