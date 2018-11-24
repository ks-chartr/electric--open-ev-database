from django.contrib import admin

from .models import *
# Register your models here.
# admin.site.register(DownloadRealData)

import csv
from django.http import HttpResponse


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


def authorise(modeladmin, request, queryset):
    queryset.update(authorised=True)


def unauthorise(modeladmin, request, queryset):
    queryset.update(authorised=False)


class DownloadRealDataAdmin(admin.ModelAdmin):
    readonly_fields = ('name', 'email', 'number', 'companyName', 'usageType', 'purpose', 'description', 'created_at', 'updated_at', )
    list_display = ['name', 'email', 'companyName', 'authorised', 'created_at']
    ordering = ['created_at', 'name']
    actions = [authorise, unauthorise, export_as_csv]
    exclude = ('passCode',)


authorise.short_description = "Authorise"
unauthorise.short_description = "Un-authorise"
export_as_csv.short_description = "Export Selected"


admin.site.register(DownloadRealData, DownloadRealDataAdmin)
