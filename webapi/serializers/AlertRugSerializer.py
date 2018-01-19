from rest_framework import serializers

from webapi.models import AlertRug, AlarmClock, MP3Playback


class AlertRugSerializer(serializers.ModelSerializer):
    is_active_first_pass = serializers.BooleanField(default=False)
    is_active_second_pass = serializers.BooleanField(default=False)
    is_playback_active = serializers.BooleanField(default=False)
    stop_seconds_hit_rug = serializers.IntegerField(min_value=0, max_value=200, default=0)
    mp3_playback = serializers.PrimaryKeyRelatedField(queryset=MP3Playback.objects.all())

    class Meta:
        model = AlertRug
        fields = ('id', 'is_active_first_pass', 'is_active_second_pass', 'is_playback_active', 
            'stop_seconds_hit_rug', 'mp3_playback')
