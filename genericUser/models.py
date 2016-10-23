# coding: utf-8
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone
from mysite.settings import BASE_DIR
import os
import datetime

ContactUsKIND = (
	(u'校對問題' , u'校對問題'),
	(u'系統問題' , u'系統問題'),
	(u'營運建議' , u'營運建議'),
	(u'加入我們' , u'加入我們'),
	(u'其他' , u'其他'),
)

class PublicFile(object):
	from mysite.settings import BASE_DIR
	def __init__(self, path):
		self.name = os.path.basename(path)
		self.path = path
		self.url = path.replace(BASE_DIR +'/static/', '')

class User(AbstractUser):
	phone = models.CharField(max_length=30)
	birthday = models.DateField()
	EDU = (
		(u'高中' , u'高中'),
		(u'學士' , u'學士'),
		(u'碩士' , u'碩士'),
	)
	education = models.CharField(max_length=30, choices=EDU)
	online = models.DateTimeField(default = timezone.now)
	org = models.ForeignKey('Organization',blank=True, null=True, on_delete=models.SET_NULL, related_name='user_set')
	status = models.IntegerField(default=0)
	STATUS = {'inactive':0, 'active':1, 'review':2}
	is_book = models.BooleanField(default=False)
	is_license = models.BooleanField(default=False)
	is_editor = models.BooleanField(default=False)
	is_guest = models.BooleanField(default=False)
	is_manager = models.BooleanField(default=False)
	is_advanced_editor = models.BooleanField(default=False)
	is_special = models.BooleanField(default=False)
	auth_email = models.BooleanField(default=False)
	auth_phone = models.BooleanField(default=False)

	def __unicode__(self):
		return self.first_name +self.last_name

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

	def authentication(self):
		return self.status == self.STATUS['active'] and self.auth_email and self.auth_phone

	def status_int2str(self):
		for k, v in self.STATUS.iteritems():
			if v == self.status:
				return k
		return 'unknown'

	def get_current_ServiceHours(self):
		month_day = datetime.date(year=datetime.date.today().year, month=datetime.date.today().month, day=1)
		try:
			current_ServiceHours = ServiceHours.objects.get(date=month_day, user=self)
		except:
			current_ServiceHours = None
		return current_ServiceHours

class Event(models.Model):
	creater = models.ForeignKey(User, related_name='event_creater_set')
	time = models.DateTimeField(auto_now_add=True)
	reviewer = models.ForeignKey(User, related_name='event_reviewer_set', blank=True, null=True)
	time_reply = models.DateTimeField(blank=True, null=True)
	status = models.IntegerField(default=0)
	message = models.CharField(max_length=100, blank=True, null=True)
	content_type = models.ForeignKey(ContentType)
	object_id = models.CharField(max_length=30)
	action = GenericForeignKey('content_type', 'object_id')
	STATUS = {'review':0, 'success':1, 'error':2}

	def status_int2str(self):
		for k, v in self.STATUS.iteritems():
			if v == self.status:
				return k
		return 'unknown'

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

class Organization(models.Model):
	name = models.CharField(max_length=50)
	address = models.CharField(max_length=100)
	email = models.EmailField()
	phone = models.CharField(max_length=30)
	manager = models.ForeignKey(User,blank=True, null=True, on_delete=models.SET_NULL, related_name='manage_org_set')
	is_service_center = models.BooleanField(default=False)

	def __unicode__(self):
		return self.name

class ServiceHours(models.Model):
	user = models.ForeignKey(User, related_name='servicehours_set')
	org = models.ForeignKey(Organization, blank=True, null=True, related_name='servicehours_set')
	date = models.DateField()
	service_hours = models.IntegerField(default=0)
	is_exchange = models.BooleanField(default=False)

	def __unicode__(self):
		return self.user.username +str(self.date)

	def get_service_hours(self):
		service_hours = 0
		for part in self.ebook_set.all():
			service_hours = service_hours +part.service_hours
		for part in self.sc_ebook_set.all():
			service_hours = service_hours +part.service_hours
		return service_hours

	def get_page_count(self):
		page_count = 0
		for part in self.ebook_set.all():
			page_count = page_count +(part.end_page -part.begin_page +1)
		for part in self.sc_ebook_set.all():
			page_count = page_count +(part.end_page -part.begin_page +1)
		return page_count

class Article(models.Model):
	author = models.ForeignKey(User,blank=True, null=True, on_delete=models.SET_NULL, related_name='article_set')
	subject = models.CharField(max_length=100)
	datetime = models.DateField(default = timezone.now)
	CATEGORY = (
		(u'公告' , u'公告'),
		(u'文件' , u'文件'),
	)
	category = models.CharField(max_length=10, choices=CATEGORY)
	path = models.CharField(max_length=255, blank=True, null=True)

	def __unicode__(self):
		return self.subject

	def get_attachment(self):
		path = os.path.join(BASE_DIR, 'static') +u'/article/{0}/attachment'.format(self.id)
		try:
			attachment_list = os.listdir(path)
		except:
			attachment_list = []
		publicFile_list = []
		for attachment in attachment_list:
			publicFile_list.append(PublicFile(os.path.join(path, attachment)))
		return publicFile_list

	def get_main_content(self):
		path = os.path.join(BASE_DIR, 'static') +u'/article/{0}/main_content.html'.format(self.id)
		return PublicFile(path)



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