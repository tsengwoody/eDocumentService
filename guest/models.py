# coding: utf-8
from django.db import models
from genericUser.models import User
from mysite import settings

class Guest(models.Model):
	user = models.OneToOneField(User, primary_key=True)
#	ID_card_number = models.CharField(max_length=10)
#	disability_card_front = models.ImageField(upload_to='disability_card')
#	disability_card_back = models.ImageField(upload_to='disability_card')

	class Meta:
		db_table = 'guest'

	def __unicode__(self):
		return self.user.username