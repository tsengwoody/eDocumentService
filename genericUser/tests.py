# coding: utf-8
from django.test import TestCase
# Create your tests here.

from django.core.urlresolvers import reverse

from account.models import Editor
from ebookSystem.models import *
from guest.models import Guest
from genericUser.models import *

class baseViewTests(TestCase):
	def setUp(self):
		p = ['active', 'editor', 'guest', 'manager', 'advanced_editor', 'root', 'license', ]
		for item in p:
			exec("permission_{0} = Permission.objects.create(name='{0}', codename='{0}')".format(item))
		root = User(username='root', email='edocumentservice@gmail.com', first_name = 'demo root firstname', last_name = 'demo root lastname', is_active=True, is_superuser=True, is_staff=True, phone='0917823099', birthday='2016-01-01', is_editor=True, is_guest=True, is_manager=True, is_advanced_editor=True, education=u'學士')
		root.set_password('root')
		root.status = root.STATUS['active']
		root.auth_email = True
		root.auth_phone = True
		root.auth_privacy = True
		root.save()
		org = Organization.objects.create(name=u'eDocumentService', address=u'台北市大同區1段149號7樓', email=u'edocumentservice@gmail.com', phone='0917823098', manager=root, is_service_center=True)
		root.org=org
		root.save()
		p = ['editor', 'guest', 'manager', 'advanced_editor', 'root', ]
		for item in p:
			exec("root.permission.add(permission_{0})".format(item))
		rootEditor = Editor.objects.create(user=root, professional_field=u'資訊工程學')
		rootGuest = Guest.objects.create(user=root)
		self.client.login(username='root', password='root')

class licenseViewTests(baseViewTests):
	def test_correct_Text_case(self):
		response = self.client.post(
			reverse(
				'genericUser:license'
			),
			{
				u'is_privacy': u'agree',
			}
		),
		root = User.objects.get(username='root')
		self.assertTrue(Permission.objects.get(codename='license') in root.permission.all())

	def test_error_Text_case(self):
		response = self.client.post(
			reverse(
				'genericUser:license'
			),
			{
			}
		),
		root = User.objects.get(username='root')
		self.assertTrue(Permission.objects.get(codename='license') in root.permission.all())

	def test_error_Text_case(self):
		response = self.client.post(
			reverse(
				'genericUser:license'
			),
			{}
		),
		root = User.objects.get(username='root')
		self.assertFalse(Permission.objects.get(codename='license') in root.permission.all())

class review_user(baseViewTests):
	def test_correct_Text_case(self):
		response = self.client.post(
			reverse(
				'genericUser:review_user',
				kwargs = {
					'username': 'root',
				}
			),
			{
				'active': 'on',
				'editor': 'on',
#				'guest': 'on',
				'review': 'success',
				'reason': '',
			}
		),
		root = User.objects.get(username='root')
		for item in ['active', 'editor', ]:
			self.assertTrue(Permission.objects.get(codename=item) in root.permission.all())
