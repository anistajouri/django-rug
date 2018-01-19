from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from webapi.models import AlertNotified
#from webapi.serializers.PlayerSerializer import AlertNotifiedSerializer


class ClickRugList(APIView):
    permission_classes = (AllowAny,)

    def update_statistics(clock, duration):
        """
        Update statistics about the click and duration
        """
        instance = AlertNotified.objects.create(date_pressed=clock,duration_Seconds=duration)
