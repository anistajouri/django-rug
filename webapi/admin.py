from django.contrib import admin
from django import forms
from django.db.models import TextField
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.utils.translation import ugettext_lazy as _
from django.utils.text import capfirst

# Integrating the model to can import and export the data via admin dashboard.
# See this docs: https://goo.gl/QR3Qqp
from import_export import resources
from import_export.admin import ImportExportModelAdmin
#from suit.widgets import AutosizedTextarea
from webapi.models import *



class AlertRugResource(resources.ModelResource):

    class Meta:
        model = AlertRug

class AlertRugAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = AlertRugResource

    list_display = ( 'id', 'is_light_active', 'is_audio_active', 'is_camera_active', 'is_message_active', 
    'stop_seconds_hit_rug', 'mp3_playback' )
    search_fields = [ 'id', 'is_light_active', 'is_audio_active', 'is_camera_active', 'is_message_active', 
    'stop_seconds_hit_rug', 'mp3_playback' ]



class AlertNotifiedResource(resources.ModelResource):

    class Meta:
        model = AlertNotified

class AlertNotifiedAdmin(ImportExportModelAdmin, admin.ModelAdmin):

    resource_class = AlertNotifiedResource

    list_display = ( 'id', 'date_pressed', 'duration_Seconds' )
    search_fields = [ 'id', 'date_pressed', 'duration_Seconds' ]

admin.site.register(AlertRug, AlertRugAdmin)
admin.site.register(AlertNotified, AlertNotifiedAdmin)