from django.db.models import *


# Create your models here.
class RegisterDataProvider(Model):
    name = CharField(max_length=100, null=True, blank=True, )
    email = CharField(max_length=100, null=True, unique=True, )
    number = CharField(max_length=100, null=True, unique=True, )
    companyName = CharField(max_length=100, null=True, blank=True, )
    description = CharField(max_length=500, null=True, blank=True, )
    passCode = CharField(max_length=100, null=True, blank=True, )
    created_at = DateTimeField(auto_now_add=True, editable=False)
    updated_at = DateTimeField(auto_now=True)
    authorised = BooleanField(default=False)
    dtl_sites = BooleanField(default=False)
    nondtl_sites = BooleanField(default=False)
    hitsToday = IntegerField(default=0)
    hitsAllTime = IntegerField(default=0)
    lastHit = DateTimeField(blank=True, null=True)

    company_website = URLField(default='http://www.example.com')
    approval_document = FileField(upload_to='approval_documents', default='default.pdf')
    operational_since = DateTimeField(blank=True, null=True)
    battery_swapping = BooleanField(default=False)
    charging = BooleanField(default=False)

    def __str__(self):
        return self.name + ', ' + str(self.authorised)
