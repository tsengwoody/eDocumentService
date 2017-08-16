# coding: utf-8
from django.db import models
from genericUser.models import User
from guest.models import Guest

'''class Editor(models.Model):
	user = models.OneToOneField(User, primary_key=True)
	professional_field = models.CharField(max_length=30, blank=True, null=True)
	class Meta:
		db_table = 'editor'

	def __unicode__(self):
		return self.user.first_name +self.user.last_name'''