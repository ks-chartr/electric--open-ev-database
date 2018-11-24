from datetime import datetime

from django.db.models import *

# Create your models here.
from django.template.backends import django


class DownloadRealData(Model):
	name = CharField(max_length=100, null=True, blank=True, editable=False)
	email = CharField(max_length=100, null=True, unique=True, editable=False)
	number = CharField(max_length=100, null=True, unique=True, editable=False)
	companyName = CharField(max_length=100, null=True, blank=True, editable=False)
	usageType = CharField(max_length=100, null=True, blank=True, editable=False)
	purpose = CharField(max_length=300, null=True, blank=True, editable=False)
	description = CharField(max_length=500, null=True, blank=True, editable=False)
	passCode = CharField(max_length=100, null=True, blank=True, editable=False)
	created_at = DateTimeField(auto_now_add=True, editable=False)
	updated_at = DateTimeField(auto_now=True)
	authorised = BooleanField(default=False)
	subscribed = BooleanField(default=False)



	def __str__(self):
		return self.name + ', ' + str(self.authorised)

