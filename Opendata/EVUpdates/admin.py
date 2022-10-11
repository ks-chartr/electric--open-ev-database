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


export_as_csv.short_description = "Export Selected"


admin.site.register(EVLocations)
