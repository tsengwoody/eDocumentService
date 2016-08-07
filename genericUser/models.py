# coding: utf-8
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone
from mysite.settings import INACTIVE, ACTIVE, EDIT, REVIEW, REVISE, FINISH
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
	online = models.DateTimeField(default = timezone.now)
	is_book = models.BooleanField(default=False)
	is_editor = models.BooleanField(default=False)
	is_guest = models.BooleanField(default=False)
	is_manager = models.BooleanField(default=False)
	is_scaner = models.BooleanField(default=False)
	status = models.IntegerField(default=REVIEW)
	STATUS = {'inactive':0, 'active':1, 'edit':2, 'review':3, 'revise':4, 'finish':5}
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
	reviewer = models.ForeignKey(User, related_name='event_reviewer_set', blank=True, null=True)
	time_reply = models.DateTimeField(blank=True, null=True)
	status = models.IntegerField(default=-1)
	message = models.CharField(max_length=100, blank=True, null=True)
	content_type = models.ForeignKey(ContentType)
	object_id = models.CharField(max_length=30)
	action = GenericForeignKey('content_type', 'object_id')
	STATUS = {'success':1, 'error':0}

	def get_url(self):
		from django.core.urlresolvers import reverse
		from ebookSystem.models import Book,EBook, ApplyDocumentAction, ReviseContentAction
		if isinstance(self.action, ApplyDocumentAction):
			return reverse('ebookSystem:review_ApplyDocumentAction', kwargs={'id':self.action.id })
		elif isinstance(self.action, Book):
			return reverse('ebookSystem:review_document', kwargs={'book_ISBN':self.action.ISBN})
		elif isinstance(self.action, EBook):
			return reverse('ebookSystem:review_part', kwargs={'ISBN_part':self.action.ISBN_part})
		elif isinstance(self.action, ReviseContentAction):
			return reverse('ebookSystem:review_ReviseContentAction', kwargs={'id':self.action.id })
		elif isinstance(self.action, User):
			return reverse('genericUser:review_user', kwargs={'username':self.action.username })

	def event_category(self):
		if isinstance(self.action, ReviseContentAction):
			return u'更正事件'
		elif isinstance(self.action, Book):
			return u'上傳文件'
		elif isinstance(self.action, ApplyDocumentAction):
			return u'代掃辨識'

	def response(self, status ,message, user):
		self.time_reply = timezone.now()
		self.reviewer = user
		if self.STATUS.has_key(status):
			self.status = self.STATUS[status]
		self.message = message
		self.save()

	def __unicode__(self):
		return self.creater.username

class Center(models.Model):
	name = models.CharField(max_length=230)
	address = models.CharField(max_length=100)
	email = models.EmailField()
	phone = models.CharField(max_length=30)
	count = models.IntegerField(default=0)

	def __unicode__(self):
		return self.name

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