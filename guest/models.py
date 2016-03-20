# coding: utf-8
from django.db import models
from genericUser.models import User
from mysite import settings

class Guest(models.Model):
	user = models.OneToOneField(User, primary_key=True)

	class Meta:
		db_table = 'guest'

	def __unicode__(self):
		return self.user.username