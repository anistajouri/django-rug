from __future__ import unicode_literals

from django.db import models

class MP3Playback(models.Model):	
    name = models.CharField(max_length=250)
    mp3_path = models.CharField(max_length=250)
    # The last started song become the default one
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return "[MP3Playback] name: %s, mp3 path: %s, is_default: %s" % (self.name, self.mp3_path, self.is_default)

class AlarmClock(models.Model):
    name = models.CharField(max_length=250)
    monday = models.BooleanField(default=False)
    tuesday = models.BooleanField(default=False)
    wednesday = models.BooleanField(default=False)
    thursday = models.BooleanField(default=False)
    friday = models.BooleanField(default=False)
    saturday = models.BooleanField(default=False)
    sunday = models.BooleanField(default=False)
    hour = models.IntegerField()
    minute = models.IntegerField()
    is_active = models.BooleanField(default=False)
    auto_stop_seconds = models.IntegerField(default=0)
    stop_seconds_hit_rug = models.IntegerField(default=0)
    mp3_playback = models.ForeignKey(MP3Playback,on_delete=models.CASCADE)


class AlertRug(models.Model):
    is_light_active = models.BooleanField(default=False)
    is_audio_active = models.BooleanField(default=False)
    is_camera_active = models.BooleanField(default=False)
    is_message_active = models.BooleanField(default=False) 
    stop_seconds_hit_rug = models.IntegerField(default=0)
    mp3_playback = models.ForeignKey(MP3Playback,on_delete=models.CASCADE)

class AlertNotified(models.Model):
    date_pressed = models.CharField(max_length=250)
    duration_Seconds = models.FloatField()


class BackupMusic(models.Model):
    backup_file = models.FileField(upload_to="backup_mp3")
