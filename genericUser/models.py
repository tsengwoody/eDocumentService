# coding: utf-8
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone
from mysite.settings import BASE_DIR

import io
import os
import shutil
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
	org = models.ForeignKey('Organization', related_name='user_set', )
	status = models.IntegerField(default=0)
	STATUS = {'inactive':0, 'active':1, 'review':2}
	is_book = models.BooleanField(default=False)
	is_license = models.BooleanField(default=False)
	is_editor = models.BooleanField(default=False)
	is_guest = models.BooleanField(default=False)
	is_manager = models.BooleanField(default=False)
	is_supermanager = models.BooleanField(default=False)
	auth_email = models.BooleanField(default=False)
	auth_phone = models.BooleanField(default=False)

	def __init__(self, *args, **kwargs):
		super(User, self).__init__(*args, **kwargs)
		self.disability_card_front = BASE_DIR +'/static/ebookSystem/disability_card/{0}/{0}_front.jpg'.format(self.username)
		self.disability_card_back = BASE_DIR +'/static/ebookSystem/disability_card/{0}/{0}_back.jpg'.format(self.username)
		self.has_disability_card = os.path.exists(BASE_DIR +'/static/ebookSystem/disability_card/{0}/'.format(self.username))

	def auth_base(self):
		return self.is_license & self.auth_email & self.auth_phone

	def auth_editor(self):
		base = self.is_license & self.auth_email & self.auth_phone
		return base & self.is_editor

	def auth_guest(self):
		base = self.is_license & self.auth_email & self.auth_phone
		from django.utils import timezone
		d = timezone.datetime(2018,9,1,tzinfo=self.date_joined.tzinfo)
		return base and self.is_guest and (self.auth_disabilitycard() or self.date_joined<d)

	def auth_disabilitycard(self):
		base = self.is_license & self.auth_email & self.auth_phone
		try:
			return base & self.disabilitycard_set.all()[0].is_active
		except:
			return False

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

class DisabilityCard(models.Model):
	identity_card_number = models.CharField(max_length=10, primary_key=True)
	owner = models.ForeignKey(User, related_name='disabilitycard_set')
	name = models.CharField(max_length=10)
	address = models.CharField(max_length=255)
	identification_date = models.DateField()
	renew_date = models.DateField()
	LEVEL = (
	(u'mild', u'輕度'),
		(u'moderate', u'中度'),
		(u'severe', u'重度'),
		(u'profound' , u'極重度'),
	)
	level = models.CharField(max_length=10, choices=LEVEL)
	CATEGORY = (
		(u'vi' , u'視障'),
	)
	category = models.CharField(max_length=10, choices=CATEGORY)
	is_active = models.BooleanField(default=False)

	def __unicode__(self):
		return self.identity_card_number

	def __init__(self, *args, **kwargs):
		super(DisabilityCard, self).__init__(*args, **kwargs)
		self.front = BASE_DIR +'/file/genericUser/DisabilityCard/{0}/{0}_front.jpg'.format(self.identity_card_number)
		self.back = BASE_DIR +'/file/genericUser/DisabilityCard/{0}/{0}_back.jpg'.format(self.identity_card_number)

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
		return ''

	def event_category(self):
		if isinstance(self.action, Book):
			return u'上傳文件'

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
	is_service_center = models.BooleanField(default=False)

	def __unicode__(self):
		return self.name

class ServiceInfo(models.Model):
	owner = models.ForeignKey(User, related_name='serviceinfo_set')
	org = models.ForeignKey(Organization, blank=True, null=True, related_name='serviceinfo_set')
	date = models.DateField()
	service_hours = models.IntegerField(default=0)
	is_exchange = models.BooleanField(default=False)

	def __unicode__(self):
		return self.owner.username +str(self.date)

	@classmethod
	def exchange_false_export(cls):
		serviceinfos = cls.objects.filter(is_exchange=False)
		export = '\t'.join([u'序號', u'帳號', u'姓名', u'起始日期', u'結束日期', u'合計時數',]) +'\r\n'
		for serviceinfo in serviceinfos:
			get_dates = [editrecord.get_date for editrecord in serviceinfo.editrecord_set.all()]
			export += '\t'.join([
				unicode(serviceinfo.id),
				serviceinfo.owner.username,
				serviceinfo.owner.first_name +serviceinfo.owner.last_name,
				unicode(min(get_dates)),
				unicode(max(get_dates)),
				unicode(serviceinfo.service_hours),
			]) + '\r\n'

		path = os.path.join(BASE_DIR, 'file', 'temp', 'serviceinfois_exchange_false_export.txt')
		dirname = os.path.dirname(path)
		if not os.path.exists(dirname):
			os.makedirs(dirname, 755)

		with io.open(path, 'w', encoding='utf-8') as f:
			f.write(export)

		return path

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
		(u'天橋說書' , u'天橋說書'),
		(u'新書推薦' , u'新書推薦'),
		(u'志工快訊' , u'志工快訊'),
		(u'校園公告' , u'校園公告'),
	)
	category = models.CharField(max_length=10, choices=CATEGORY)

	def __init__(self, *args, **kwargs):
		super(Announcement, self).__init__(*args, **kwargs)
		self.path = BASE_DIR +'/file/genericUser/Announcement/{0}/'.format(self.id)

	def __unicode__(self):
		return self.title

	def delete(self, *args, **kwargs):
		try:
			shutil.rmtree(self.path)
		except:
			pass
		super(Announcement, self).delete(*args, **kwargs)

class QAndA(models.Model):
	question = models.TextField()
	answer = models.TextField()
	order = models.IntegerField()
	CATEGORY = (
		(u'platform' , u'平台'),
		(u'volunteer', u'志工'),
		(u'vip', u'視障者'),
		(u'tutorial', u'教學'),
	)
	category = models.CharField(max_length=10, choices=CATEGORY)

	def __unicode__(self):
		return unicode(self.id)

class BusinessContent(models.Model):
	name = models.CharField(max_length=100, primary_key=True)
	content = models.TextField()

class BannerContent(models.Model):
	title = models.CharField(max_length=100, )
	content = models.TextField()
	order = models.IntegerField()
	url = models.CharField(max_length=255, blank=True, null=True)

	def __init__(self, *args, **kwargs):
		super(BannerContent, self).__init__(*args, **kwargs)
		self.cover_image = BASE_DIR +'/file/genericUser/BannerContent/{0}/cover/image.jpg'.format(self.id)

	def __unicode__(self):
		return unicode(self.id)

	def delete(self, *args, **kwargs):
		try:
			path = os.path.dirname(os.path.dirname(self.cover_image))
			shutil.rmtree(path)
		except:
			pass
		super(BannerContent, self).delete(*args, **kwargs)
