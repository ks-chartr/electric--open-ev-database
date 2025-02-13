from datetime import datetime

from django.db.models import *

# Create your models here.
from django.template.backends import django


class DownloadRealData(Model):
	name = CharField(max_length=100, null=True, blank=True,)
	email = CharField(max_length=100, null=True, unique=True,)
	number = CharField(max_length=100, null=True, unique=True,)
	companyName = CharField(max_length=100, null=True, blank=True,)
	usageType = CharField(max_length=100, null=True, blank=True,)
	purpose = CharField(max_length=300, null=True, blank=True,)
	description = CharField(max_length=500, null=True, blank=True,)
	passCode = CharField(max_length=100, null=True, blank=True,)
	created_at = DateTimeField(auto_now_add=True, editable=False)
	updated_at = DateTimeField(auto_now=True)
	authorised = BooleanField(default=False)
	subscribed = BooleanField(default=False)
	hitsToday = IntegerField(default=0)
	hitsAllTime = IntegerField(default=0)
	lastHit = DateTimeField(blank=True, null=True)

	def __str__(self):
		return self.name + ', ' + str(self.authorised)

