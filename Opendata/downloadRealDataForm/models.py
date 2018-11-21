from django.db.models import *

# Create your models here.

class DownloadRealData(Model):
	name = CharField(max_length=100, null=True, blank=True)
	email = CharField(max_length=100, null=True, unique=True)
	number = CharField(max_length=100, null=True, unique=True)
	companyName = CharField(max_length=100, null=True, blank=True)
	usageType = CharField(max_length=100, null=True, blank=True)
	purpose = CharField(max_length=300, null=True, blank=True)
	description = CharField(max_length=500, null=True, blank=True)
	passCode = CharField(max_length=100, null=True, blank=True)
	authorised = BooleanField(default=False)
	subscribed = BooleanField(default=False)

	def __str__(self):
		return self.name + ' ' + str(self.authorised)

