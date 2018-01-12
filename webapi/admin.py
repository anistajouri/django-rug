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

    list_display = ( 'is_active_first_pass', 'is_active_second_pass', 'is_playback_active', 
    'alert_duration_Seconds', 'auto_stop_seconds',  'stop_seconds_hit_rug', 'mp3_playback' )
    search_fields = [ 'name', 'is_active_first_pass', 'is_active_second_pass', 'is_playback_active', 
    'alert_duration_Seconds', 'auto_stop_seconds',  'stop_seconds_hit_rug', 'mp3_playback' ]



admin.site.register(AlertRug, AlertRugAdmin)