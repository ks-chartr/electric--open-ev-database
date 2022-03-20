from django.db.models import *


# Create your models here.
class EVLocations(Model):
    uid = CharField(max_length=100, null=True, blank=True, )
    name = CharField(max_length=100, null=True, blank=True, )
    vendor_name = CharField(max_length=100, null=True, blank=True, )
    address = CharField(max_length=100, null=True, blank=True, )
    latitude = FloatField(null=True, blank=True, )
    longitude = FloatField(null=True, blank=True, )
    charger_type = TextField(null=True, blank=True, )
    city = CharField(max_length=100, null=True, blank=True, )
    country = CharField(max_length=100, null=True, blank=True, )
    open = CharField(max_length=100, null=True, blank=True, )
    close = CharField(max_length=100, null=True, blank=True, )
    logo_url = TextField(null=True, blank=True, )
    staff = CharField(max_length=100, null=True, blank=True, )
    total = CharField(max_length=100, null=True, blank=True, )
    available = CharField(max_length=100, null=True, blank=True, )
    cost_per_unit = CharField(max_length=100, null=True, blank=True, )
    payment_modes = CharField(max_length=100, null=True, blank=True, )
    contact_numbers = CharField(max_length=100, null=True, blank=True, )
    provider_passcode = CharField(max_length=100, null=True, blank=True, )

    def __str__(self):
        return self.name + ', ' + str(self.uid) + ', ' + str(self.provider_passcode)
