from rest_framework import serializers

from webapi.models import MP3Playback


class PlayerManagerSerializer(serializers.Serializer):
    status = serializers.CharField()
    mp3_playback = serializers.PrimaryKeyRelatedField(required=False,
                                                  queryset=MP3Playback.objects.all(),
                                                  allow_empty=True)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass



