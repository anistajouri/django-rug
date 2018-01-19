from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

#from webapi.Utils.SoundManager import SoundManager
from webapi.serializers.SoundManagerSerializer import SoundManagerSerializer

#for testing
from webapi.rug_manage_win import start_rug_manage


class VolumeManagement(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        """
        Get the volume status
        """
        #content = {'volume': SoundManager.get_volume()}
        content = {'volume': 50}
        return Response(content)

    def post(self, request):
        start_rug_manage("start") 
        serializer = SoundManagerSerializer(data=request.data)

        if serializer.is_valid():
            #SoundManager.set_volume(serializer.validated_data["volume"])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
