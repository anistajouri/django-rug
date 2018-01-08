from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from webapi.Utils.PlayerManager import PlayerManager
from webapi.models import MP3Playback
from webapi.serializers.PlayerSerializer import PlayerManagerSerializer


class PlayerStatus(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        """
        Get the Mplayer status
        """
        if PlayerManager.is_started():
            status = "on"
        else:
            status = "off"

        answer = {
            "status": status
        }
        return Response(answer)

    def post(self, request):
        serializer = PlayerManagerSerializer(data=request.data)

        if serializer.is_valid():
            new_status = serializer.validated_data["status"]
            if new_status == "on":
                # give a mp3 playback to play is optional
                if "mp3_playback" in serializer.validated_data:
                    mp3_playback = serializer.validated_data["mp3_playback"]

                    mp3_to_play = mp3_playback.mp3_path
                    # remove the is_default from other mp3 playback
                    qs = MP3Playback.objects.filter(is_default=True)
                    qs.update(is_default=False)
                    # the selected mp3 playback become the default one
                    mp3_playback.is_default = True
                    mp3_playback.save()

                else:
                    # get the default mp3 playback if exist
                    try:
                        default_mp3_playback = MP3Playback.objects.get(is_default=True)
                        mp3_to_play = default_mp3_playback.mp3_path
                    except MP3Playback.DoesNotExist:
                        # No default mp3 playback
                        answer = {
                            "status": "error, no default mp3 playback"
                        }
                        return Response(answer, status=status.HTTP_400_BAD_REQUEST)
                PlayerManager.play(mp3_to_play)
                returned_status = "on"
            else:
                PlayerManager.stop()
                returned_status = "off"

            answer = {
                "status": returned_status
            }
            return Response(answer)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
