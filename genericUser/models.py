# coding: utf-8
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone
#from ebookSystem.models import Book,EBook
from mysite.settings import PREFIX_PATH,INACTIVE, ACTIVE, EDIT, REVIEW, REVISE, FINISH
import os
import datetime

EDU = (
	(u'高中' , u'高中'),
	(u'學士' , u'學士'),
	(u'碩士' , u'碩士'),
)

ContactUsKIND = (
	(u'校對問題' , u'校對問題'),
	(u'系統問題' , u'系統問題'),
	(u'營運建議' , u'營運建議'),
	(u'加入我們' , u'加入我們'),
	(u'其他' , u'其他'),
)

class User(AbstractUser):
	phone = models.CharField(max_length=30)
	birthday = models.DateField()
	education = models.CharField(max_length=30, choices=EDU)
	online = models.DateTimeField(blank=True, null=True)
	is_book = models.BooleanField(default=False)
	is_editor = models.BooleanField(default=False)
	is_guest = models.BooleanField(default=False)
	is_manager = models.BooleanField(default=False)
	is_scaner = models.BooleanField(default=False)
	status = models.IntegerField(default=REVIEW)

	def __unicode__(self):
		return self.username

	def has_editor(self):
		try:
			self.editor
			return True
		except:
			return False

	def has_guest(self):
		try:
			self.guest
			return True
		except:
			return False

class Event(models.Model):
	creater = models.ForeignKey(User, related_name='event_creater_set')
	time = models.DateTimeField(auto_now_add=True)
#	review_url = models.CharField(max_length=100, blank=True, null=True)
	reviewer = models.ForeignKey(User, related_name='event_reviewer_set', blank=True, null=True)
	status = models.IntegerField(default=0)
	message = models.CharField(max_length=100, blank=True, null=True)
	event_category = (
		(u'上傳審核' , u'上傳審核'),
		(u'校對審核' , u'校對審核'),
		(u'會員審核' , u'會員審核'),
		(u'聯絡我們' , u'聯絡我們'),
		(u'更正校對' , u'更正校對'),
	)
	category = models.CharField(max_length=10, choices=event_category)
	content_type = models.ForeignKey(ContentType)
	object_id = models.CharField(max_length=30)
	action = GenericForeignKey('content_type', 'object_id')

	def __unicode__(self):
		return self.creater.username

class ContactUs(models.Model):
	name = models.CharField(max_length=10)
	email = models.EmailField()
	message_datetime = models.DateField(default = timezone.now)
	kind = models.CharField(max_length=10, choices=ContactUsKIND)
	subject = models.CharField(max_length=50)
	content = models.CharField(max_length=1000)
	def __unicode__(self):
		return self.subject

class Reply(models.Model):
	contact_us = models.ForeignKey(ContactUs)
	message_datetime = models.DateField()
	content = models.CharField(max_length=1000)
	def __unicode__(self):
		return self.message_datetime