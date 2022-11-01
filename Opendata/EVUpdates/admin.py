from django.contrib import admin

from .models import *
# Register your models here.
# admin.site.register(DownloadRealData)

import csv
from django.http import HttpResponse
from django.core.mail import send_mail


def export_as_csv(self, request, queryset):

    meta = self.model._meta
    field_names = [field.name for field in meta.fields]

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
    writer = csv.writer(response)

    writer.writerow(field_names)
    for obj in queryset:
        row = writer.writerow([getattr(obj, field) for field in field_names])

    return response


class EVLocationsAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'vendor', 'address']
    ordering = ['vendor']
    actions = [export_as_csv]


class ConnectorMappingAdmin(admin.ModelAdmin):
    list_display = ['vendor_connector_name', 'mapped_connector_name']
    ordering = ['mapped_connector_name']
    actions = [export_as_csv]


export_as_csv.short_description = "Export Selected"


admin.site.register(EVLocations, EVLocationsAdmin)
admin.site.register(ConnectorMapping, ConnectorMappingAdmin)
