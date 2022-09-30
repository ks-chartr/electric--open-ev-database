from django.core.exceptions import ValidationError
from django.db.models import *


# Create your models here.
class EVLocations(Model):
    def charger_type_validator(self, charger_type):
        for field in ["available", "capacity", "cost_per_unit", "count", "diagram", "total", "type"]:
            if field not in charger_type.keys():
                raise ValidationError(f"{field} not given in charger type")

    def coordinates_validator(self, coordinates):
        for field in ['latitude', 'longitude']:
            if field not in coordinates.keys():
                raise ValidationError(f"{field} not given in charger type")

    id = CharField(max_length=100, blank=True, primary_key=True)
    name = CharField(max_length=100, null=True, blank=True, )
    vendor = CharField(max_length=100, null=True, blank=True, )
    address = CharField(max_length=100, null=True, blank=True, )
    coordinates = CharField(max_length=100, null=True, blank=True, )
    charger_type = TextField(null=True, blank=True, )
    city = CharField(max_length=100, null=True, blank=True, )
    country = CharField(max_length=100, null=True, blank=True, )
    open = CharField(max_length=100, null=True, blank=True, )
    close = CharField(max_length=100, null=True, blank=True, )
    logo = TextField(null=True, blank=True, )
    staff = CharField(max_length=100, null=True, blank=True, )
    total = CharField(max_length=100, null=True, blank=True, )
    available = CharField(max_length=100, null=True, blank=True, )
    payment_modes = CharField(max_length=100, null=True, blank=True, )
    contact_numbers = CharField(max_length=100, null=True, blank=True, )
    provider_passcode = CharField(max_length=100, null=True, blank=True, )
    postal_code = CharField(max_length=100, null=True, blank=True, )
    dtl_site = BooleanField(default=True)
    station_type = CharField(max_length=100, default="charging")

    def __str__(self):
        return self.name + ', ' + str(self.id) + ', ' + str(self.provider_passcode)
