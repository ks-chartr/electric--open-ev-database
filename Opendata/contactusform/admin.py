from django.contrib import admin
from .models import *

# admin.site.register(Terms)
admin.site.register(Policy)
admin.site.register(EVLastUpdated)


class TermsAdmin(admin.ModelAdmin):
    change_form_template = 'contactusform/admin/change_form.html'


class ContactRequestAdmin(admin.ModelAdmin):
    readonly_fields = ('name', 'email', 'subject', 'message')
    list_display = ['name', 'email', 'subject', 'message', 'created_at']
    ordering = ['created_at', 'name']


class DownloadDataAdmin(admin.ModelAdmin):
    readonly_fields = ('name', 'email', 'usageType', 'purpose', 'created_at', 'dataDownloaded')
    list_display = ['name', 'email', 'usageType', 'dataDownloaded', 'purpose', 'created_at']
    ordering = ['created_at', 'dataDownloaded']


class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['message', 'published', 'createdAt']
    ordering = ['createdAt',]


admin.site.register(DownloadData, DownloadDataAdmin)
admin.site.register(ContactRequest, ContactRequestAdmin)
admin.site.register(Announcement, AnnouncementAdmin)
admin.site.register(Terms, TermsAdmin)
