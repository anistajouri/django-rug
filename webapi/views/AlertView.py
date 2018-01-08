from django.http import Http404
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from webapi.Utils.CrontabManager import CrontabManager
from webapi.models import Alert
from webapi.serializers.AlertRugSerializer import AlertRugSerializer
from webapi.views import Utils


class AlertList(APIView):
    permission_classes = (AllowAny,)
    serializer_class = AlertSerializer

    def get(self, request, format=None):
        alerts = Alert.objects.all()
        serializer = AlertSerializer(alerts, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = AlertSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # create a job line
            last_alert = Alert.objects.latest('id')
            Utils.add_job_in_crontab(last_alert)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AlertDetail(APIView):
    """
    Retrieve, update or delete a WebRadio instance.
    """
    permission_classes = (AllowAny,)
    serializer_class = AlertSerializer

    def get_object(self, pk):
        try:
            return Alert.objects.get(pk=pk)
        except Alert.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        alert = self.get_object(pk)
        serializer = AlertSerializer(alert)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        alert = self.get_object(pk)
        serializer = AlertSerializer(alert, data=request.data)
        if serializer.is_valid():
            serializer.save()
            updated_alert = Alert.objects.get(pk=pk)
            # remove the job from the crontab
            job_comment = "alertrug%s" % updated_alert.id
            CrontabManager.remove_job(job_comment)
            # add it back with new info
            Utils.add_job_in_crontab(updated_alert)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        alert = self.get_object(pk)
        # remove the line from the crontab
        job_comment = "alertrug%s" % alert.id
        CrontabManager.remove_job(job_comment)
        # remove from the database
        alert.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
