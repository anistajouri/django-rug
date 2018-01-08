from rest_framework import serializers

from webapi.models import MP3Playback

class MP3PlaybackSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, allow_blank=False, max_length=250)
    mp3_path = serializers.CharField(required=True, allow_blank=False, max_length=250)
    is_default = serializers.BooleanField(default=False)

    class Meta:
        model = MP3Playback
        fields = ('id', 'name', 'mp3_path', 'is_default')
