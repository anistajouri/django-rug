from django.http import Http404
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from webapi.Utils.CrontabManager import CrontabManager
from webapi.models import MP3Playback, AlarmClock
from webapi.serializers.MP3PlaybackSerializer import MP3PlaybackSerializer


class MP3PlaybackList(APIView):
    permission_classes = (AllowAny,)
    serializer_class = MP3PlaybackSerializer

    def get(self, request, format=None):
        mp3playbacks = MP3Playback.objects.all()
        serializer = MP3PlaybackSerializer(mp3playbacks, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = MP3PlaybackSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MP3PlaybackDetail(APIView):
    """
    Retrieve, update or delete a MP3Playback instance.
    """
    def get_object(self, pk):
        try:
            return MP3Playback.objects.get(pk=pk)
        except MP3Playback.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        mp3playback = self.get_object(pk)
        serializer = MP3PlaybackSerializer(mp3playback)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        mp3playback = self.get_object(pk)
        serializer = MP3PlaybackSerializer(mp3playback, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        mp3playback = self.get_object(pk)
        # when we delete a web radio, all alarm based on this on will be deleted to, remove them from the contab before
        all_alarms_which_use_the_web_radio_to_delete = AlarmClock.objects.filter(mp3playback=mp3playback)
        for alarm in all_alarms_which_use_the_web_radio_to_delete:
            # remove the job from the crontab
            job_comment = "alertrug%s" % alarm.id
            CrontabManager.remove_job(job_comment)
        # then we can safely delete the web radio
        mp3playback.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
