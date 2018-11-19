from django.contrib import admin

from .models import *
# Register your models here.
admin.site.register(DownloadRealData)
# class DownloadRealDataAdmin(admin.ModelAdmin):
    # exclude = ('passCode',)

# admin.site.register(DownloadRealData, DownloadRealDataAdmin)
