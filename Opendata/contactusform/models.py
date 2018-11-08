# Create your models here.
from django.db.models import * 
from tinymce.models import HTMLField

class ContactRequest(Model):
	name = CharField(max_length=100, default="Unknown")
	email = CharField(max_length=100)
	subject = CharField(max_length=100)
	message = TextField()
	def __str__(self):
		return self.email


class Terms(Model):
	text = CharField(max_length=200)
	content = HTMLField()
	def __str__(self):
		return self.text

class Policy(Model):
	text = CharField(max_length=200)
	def __str__(self):
		return self.text


class RoutesLastUpdated(Model):
	text = CharField(max_length=100, default='routes last updated')
	date = DateField()
	def __str__(self):
		return self.text
class StopTimeLastUpdated(Model):
	text = CharField(max_length=100, default='stop time last updated')
	date = DateField()
	def __str__(self):
		return self.text
class TripsLastUpdated(Model):
	text = CharField(max_length=100, default='Trips last updated')
	date = DateField()
	def __str__(self):
		return self.text
class StopLastUpdated(Model):
	text = CharField(max_length=100, default='Stop last updated')
	date = DateField()
	def __str__(self):
		return self.text
class DownloadData(Model):
	name = CharField(max_length=100, null=True, default='')
	email = CharField(max_length=100, null=True, default='')
	usageType = CharField(max_length=100, null=True, default='')
	purpose = CharField(max_length=300, null=True, default='')
	dataDownloaded = CharField(max_length=100, null=True, default='')
	def __str__(self):
		return self.name + ' ' +self.usageType




