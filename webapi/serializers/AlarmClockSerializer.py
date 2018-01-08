from rest_framework import serializers

from webapi.models import AlarmClock, MP3Playback


class AlarmClockSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=250)
    monday = serializers.BooleanField(default=False)
    tuesday = serializers.BooleanField(default=False)
    wednesday = serializers.BooleanField(default=False)
    thursday = serializers.BooleanField(default=False)
    friday = serializers.BooleanField(default=False)
    saturday = serializers.BooleanField(default=False)
    sunday = serializers.BooleanField(default=False)
    hour = serializers.IntegerField(min_value=0, max_value=23)
    minute = serializers.IntegerField(min_value=0, max_value=59)
    is_active = serializers.BooleanField(default=False)
    auto_stop_seconds = serializers.IntegerField(min_value=0, max_value=200, default=0)
    stop_seconds_hit_rug = serializers.IntegerField(min_value=0, max_value=200, default=0)
    mp3_playback = serializers.PrimaryKeyRelatedField(queryset=MP3Playback.objects.all())

    class Meta:
        model = AlarmClock
        fields = ('id', 'name', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'hour',
                  'minute', 'auto_stop_seconds', 'stop_seconds_hit_rug', 'is_active', 'mp3_playback')
