from django.contrib import admin

from .models import *
# Register your models here.

import csv
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings


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
    print('authorising')
    for user_queryset in queryset:
        subject = 'Welcome to Delhi Government Open Database for EV Charging'
        message = f"Dear {user_queryset.name}\nThank you for registering {user_queryset.companyName} on Delhi Government's Open Database for EV Charging and Swapping Stations.\n\nYour API key has been authorised.\n\nThe Open Database for EV charging is an initiative for creating one platform for discovering all EV chargers and Battery Swapping stations in Delhi. We look forward to your support in ensuring the data provided is up to date and pertains only to public charging and swapping stations.\n\nIn case of any query, please mail on delhievcell@gmail.com.\nThanks & Regards\nState EV cell, Delhi"
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [user_queryset.email, ]
        send_mail(subject, message, email_from, recipient_list)
    queryset.update(authorised=True)


def unauthorise(modeladmin, request, queryset):
    print('unauthorising')
    # for user_queryset in queryset:
    #     send_mail(
    #         'Delhi Open EV Database API key Unauthorization',
    #         'Sorry! \nYour API key has been unauthorized.',
    #         'delhievdb@ev.delhitransport.in',
    #         [f'{user_queryset.email}'],
    #         fail_silently=False,
    #     )
    queryset.update(authorised=False)


class RegisterDataProviderAdmin(admin.ModelAdmin):
    readonly_fields = (
    'name', 'email', 'number', 'companyName', 'description', 'created_at', 'updated_at', 'hitsToday', 'hitsAllTime',
    'lastHit', 'dtl_sites', 'nondtl_sites', 'operational_since', 'company_website', 'authorised')
    list_display = ['name', 'email', 'companyName', 'authorised', 'created_at', 'lastHit', 'hitsAllTime', 'dtl_sites', 'nondtl_sites']
    ordering = ['created_at', 'name']
    actions = [authorise, unauthorise, export_as_csv]
    exclude = ('passCode',)


authorise.short_description = "Authorise"
unauthorise.short_description = "Un-authorise"
export_as_csv.short_description = "Export Selected"

admin.site.register(RegisterDataProvider, RegisterDataProviderAdmin)
