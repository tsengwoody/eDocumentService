# coding: utf-8
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone
from mysite.settings import BASE_DIR
import os
import datetime

def generic_serialized(self):
	serialize = {}
	for field in self._meta.fields:
		value = getattr(self, field.name)
		if isinstance(value, models.Model):
			id_ = field.name +'_id'
			field_id_value = getattr(self, id_)
			value = '{0}/{1}'.format(value.__class__.__name__, field_id_value)
		else:
			try:
				json.dumps(value)
			except:
				value = unicode(value)
		serialize.update({field.name: value})
	return serialize

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
	(u'國小' , u'國小'),
	(u'國中' , u'國中'),
		(u'高中' , u'高中'),
		(u'學士' , u'學士'),
		(u'碩士' , u'碩士'),
	)
	education = models.CharField(max_length=30, choices=EDU)
	online = models.DateTimeField(default = timezone.now)
	org = models.ForeignKey('Organization',blank=True, null=True, on_delete=models.SET_NULL, related_name='user_set', )
	status = models.IntegerField(default=0)
	STATUS = {'inactive':0, 'active':1, 'review':2}
	is_book = models.BooleanField(default=False)
	is_license = models.BooleanField(default=False)
	is_editor = models.BooleanField(default=False)
	is_guest = models.BooleanField(default=False)
	is_manager = models.BooleanField(default=False)
	is_advanced_editor = models.BooleanField(default=False)
	auth_email = models.BooleanField(default=False)
	auth_phone = models.BooleanField(default=False)

	def __init__(self, *args, **kwargs):
		super(User, self).__init__(*args, **kwargs)
		self.disability_card_front = BASE_DIR +'/static/ebookSystem/disability_card/{0}/{0}_front.jpg'.format(self.username)
		self.disability_card_back = BASE_DIR +'/static/ebookSystem/disability_card/{0}/{0}_back.jpg'.format(self.username)
		self.has_disability_card = os.path.exists(BASE_DIR +'/static/ebookSystem/disability_card/{0}/'.format(self.username))

	def __unicode__(self):
		return self.first_name +self.last_name

	def serialized(self, action):
		old_serialize = generic_serialized(self)
		serialize = {}
		if action == 'info':
			for key in [
				'id',
				'username',
				'email',
				'first_name',
				'last_name',
				'phone',
				'birthday',
				'education',
				'is_book',
				'org',
			]:
				serialize.update({
					key: old_serialize[key],
				})

		elif action == 'role':
			for key in [
				'id',
				'auth_phone',
				'auth_email',
				'is_active',
				'is_editor',
				'is_guest',
			]:
				serialize.update({
					key: old_serialize[key],
				})

		elif action == 'disability_card':
			import base64
			try:
				with open(self.disability_card_front, 'rb') as f:
					front = f.read()
					front = base64.b64encode(front)
			except BaseException as e:
				front = ''

			try:
				with open(self.disability_card_back, 'rb') as f:
					back = f.read()
					back = base64.b64encode(back)
			except BaseException as e:
				back = ''

			serialize = {
				'id': self.id,
				'front': front,
				'back': back,
			}

		return serialize

	def authentication(self):
		return self.auth_email and self.auth_phone and self.is_license

	def status_int2str(self):
		for k, v in self.STATUS.iteritems():
			if v == self.status:
				return k
		return 'unknown'

	def get_current_ServiceInfo(self):
		month_day = datetime.date(year=datetime.date.today().year, month=datetime.date.today().month, day=1)
		try:
			current_ServiceInfo = ServiceInfo.objects.get(date=month_day, user=self)
		except:
			current_ServiceInfo = None
		return current_ServiceInfo

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
		from ebookSystem.models import *
		if isinstance(self.action, Book):
			return reverse('ebookSystem:review_document', kwargs={'book_ISBN':self.action.ISBN})
		elif isinstance(self.action, EBook):
			return reverse('ebookSystem:review_part', kwargs={'ISBN_part':self.action.ISBN_part})
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
		self.status = self.STATUS[status]
		self.message = unicode(self.action) +message
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

class ServiceInfo(models.Model):
	user = models.ForeignKey(User, related_name='serviceinfo_set')
	org = models.ForeignKey(Organization, blank=True, null=True, related_name='serviceinfo_set')
	date = models.DateField()
	service_hours = models.IntegerField(default=0)
	is_exchange = models.BooleanField(default=False)

	def __unicode__(self):
		return self.user.username +str(self.date)

	def get_stay_hours(self):
		stay_hours = 0
		for editRecord in self.editrecord_set.all():
			stay_hours = stay_hours +editRecord.stay_hours
		return stay_hours

	def get_service_hours(self):
		service_hours = 0
		for editRecord in self.editrecord_set.all():
			service_hours = service_hours +editRecord.service_hours
		return service_hours

	def get_page_count(self):
		page_count = 0
		for editRecord in self.editrecord_set.all():
			try:
				page_count = page_count +(editRecord.part.end_page -editRecord.part.begin_page +1)
			except:
				pass
		return page_count

	def get_character_count(self):
		character_count = 0
		for editRecord in self.editrecord_set.all():
			try:
				i = editRecord.part.get_character_count()
			except:
				i=0
			character_count = character_count +i
		return character_count

class Announcement(models.Model):
	title = models.CharField(max_length=100)
	content = models.TextField()
	datetime = models.DateField(default = timezone.now)
	CATEGORY = (
		(u'平台消息' , u'平台消息'),
		(u'新書推薦' , u'新書推薦'),
		(u'志工快訊' , u'志工快訊'),
	)
	category = models.CharField(max_length=10, choices=CATEGORY)

	def __unicode__(self):
		return self.title

class QAndA(models.Model):
	question = models.TextField()
	answer = models.TextField()
	order = models.IntegerField()

	def __unicode__(self):
		return self.id

class BusinessContent(models.Model):
	name = models.CharField(max_length=100, )
	content = models.TextField()

class BannerContent(models.Model):
	title = models.CharField(max_length=100, )
	content = models.TextField()
	order = models.IntegerField()

	def __unicode__(self):
		return self.id
