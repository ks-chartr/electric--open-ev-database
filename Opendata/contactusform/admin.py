from django.contrib import admin
from .models import *
admin.site.register(ContactRequest)
admin.site.register(Terms)
admin.site.register(Policy)
admin.site.register(RoutesLastUpdated)
admin.site.register(StopTimeLastUpdated)
admin.site.register(TripsLastUpdated)
admin.site.register(StopLastUpdated)