# Create your models here.
from django.db.models import * 

class ContactRequest(Model):
	email = CharField(max_length=100)
	phone = CharField(max_length=100)
	message = TextField()
	def __unicode__(self):
		return self.email