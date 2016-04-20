# coding: utf-8
from django.db import models
from genericUser.models import User
from mysite import settings

class Editor(models.Model):
	user = models.OneToOneField(User, primary_key=True)
	service_hours = models.IntegerField(default=0)
	professional_field = models.CharField(max_length=30, blank=True, null=True)
	class Meta:
		db_table = 'editor'

	def __unicode__(self):
		return self.user.username