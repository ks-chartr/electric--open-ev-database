from django.contrib import admin
from .models import *
admin.site.register(ContactRequest)
# admin.site.register(Terms)
admin.site.register(Policy)
admin.site.register(RoutesLastUpdated)
admin.site.register(StopTimeLastUpdated)
admin.site.register(TripsLastUpdated)
admin.site.register(StopLastUpdated)

class TermsAdmin(admin.ModelAdmin):
    change_form_template = 'contactusform/admin/change_form.html'

admin.site.register(Terms, TermsAdmin)