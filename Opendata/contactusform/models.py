# Create your models here.
from django.db.models import * 

class ContactRequest(Model):
	email = CharField(max_length=100)
	phone = CharField(max_length=100)
	message = TextField()
	def __str__(self):
		return self.email


class Terms(Model):
	text = CharField(max_length=200)
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
