# Create your models here.
from django.db.models import *
from tinymce.models import HTMLField


class ContactRequest(Model):
	name = CharField(max_length=100, default="Unknown")
	email = CharField(max_length=100)
	subject = CharField(max_length=100)
	created_at = DateTimeField(auto_now_add=True,)
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


class EVLastUpdated(Model):
	text = CharField(max_length=100, default='EV static data last updated')
	date = DateField()

	def __str__(self):
		return self.text


class DownloadData(Model):
	name = CharField(max_length=100, null=True, default='')
	email = CharField(max_length=100, null=True, default='')
	usageType = CharField(max_length=100, null=True, default='')
	purpose = CharField(max_length=300, null=True, default='')
	dataDownloaded = CharField(max_length=100, null=True, default='')
	created_at = DateTimeField(auto_now_add=True,)

	def __str__(self):
		return self.name + ' ' + self.usageType


class Announcement(Model):
	createdAt = DateTimeField(auto_now_add=True)
	message = CharField(max_length=500, null=True, blank=True,)
	published = BooleanField(default=True)

	def __str__(self):
		return self.message
