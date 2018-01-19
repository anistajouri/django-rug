from django.http import Http404
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from webapi.Utils.CrontabManager import CrontabManager
from webapi.models import AlertRug
from webapi.serializers.AlertRugSerializer import AlertRugSerializer
from webapi.views import Utils


# class AlertList(APIView):
#     permission_classes = (AllowAny,)
#     serializer_class = AlertSerializer

#     def get(self, request, format=None):
#         alerts = Alert.objects.all()
#         serializer = AlertSerializer(alerts, many=True)
#         return Response(serializer.data)

#     def post(self, request, format=None):
#         serializer = AlertSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             # create a job line
#             last_alert = Alert.objects.latest('id')
#             Utils.add_job_in_crontab(last_alert)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class AlertRugConfig(APIView):
    permission_classes = (AllowAny,)

    def get_object(self, pk):
        try:
            return AlertRug.objects.get(pk=pk)
        except AlertRug.DoesNotExist:
            raise Http404


    def put(self, request, pk, format=None):
        alertrug = self.get_object(pk)
        serializer = AlertRugSerializer(alertrug, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def get(self, request, pk, format=None):
        alertrug = self.get_object(pk)
        serializer = AlertRugSerializer(alertrug)
        return Response(serializer.data)

    def post(self, request):
        serializer = AlertRugSerializer(data=request.data)

        if serializer.is_valid():
            stop_seconds_hit_rug = serializer.validated_data["stop_seconds_hit_rug"]
            print("stop_seconds_hit_rug=============", stop_seconds_hit_rug)
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
