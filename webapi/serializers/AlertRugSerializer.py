from rest_framework import serializers

from webapi.models import AlertRug, AlarmClock, MP3Playback


class AlertRugSerializer(serializers.ModelSerializer):
    is_light_active = serializers.BooleanField(default=False)
    is_audio_active = serializers.BooleanField(default=False)
    is_camera_active = serializers.BooleanField(default=False)
    is_message_active = serializers.BooleanField(default=False) 
    stop_seconds_hit_rug = serializers.IntegerField(min_value=0, max_value=200, default=0)
    mp3_playback = serializers.PrimaryKeyRelatedField(queryset=MP3Playback.objects.all())

    class Meta:
        model = AlertRug
        fields = ('id', 'is_light_active', 'is_audio_active', 'is_camera_active', 'is_message_active', 
            'stop_seconds_hit_rug', 'mp3_playback')
