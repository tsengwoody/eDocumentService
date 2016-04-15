# coding: utf-8
from django.core import mail
from django.core.urlresolvers import reverse
from django.http import HttpRequest,HttpResponse
from django.test import Client, RequestFactory, TestCase, TransactionTestCase
from account.models import *
from ebookSystem.models import *
from genericUser.models import *
from guest.models import *
from .views import *
from mysite import settings
import os
import shutil

class contact_usTestCase(TransactionTestCase):
	@classmethod
	def setUpClass(cls):
		super(contact_usTestCase, cls).setUpClass()
		user = User(username='testcase', is_active=True, phone='1234567890', birthday='2016-01-01')
		user.set_password('root')
		user.save()
		cls.user = user
		cls.factory = RequestFactory()

	def test_contact_us_normal(self):
		self.client = Client()
		c = self.client.login(username='testcase', password='root')
		self.assertTrue(c)
#		request = self.factory.post(reverse('genericUser:contact_us'), {'name':u'曾奕勳', 'email':'tsengwoody@yahoo.com.tw', 'kind':u'校對問題', 'subject':u'請問流程圖輸入', 'content':u'你好：\n\n想請問\n\n以上'})
#		request.user = self.user
#		response = contact_us(request, )
		response = self.client.post(reverse('genericUser:contact_us'), {'name':u'曾奕勳', 'email':'tsengwoody@yahoo.com.tw', 'kind':u'校對問題', 'subject':u'請問流程圖輸入', 'content':u'你好：\n\n想請問\n\n以上'}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
		self.assertEqual(response.status_code,200)
		self.assertEqual(len(ContactUs.objects.all()),1)
		self.assertEqual(len(mail.outbox), 1)
		contactUs = ContactUs.objects.first()
		print mail.outbox[0].body

	@classmethod
	def tearDownClass(cls):
		super(contact_usTestCase, cls).tearDownClass()

class registerTestCase(TransactionTestCase):
	@classmethod
	def setUpClass(cls):
		super(registerTestCase, cls).setUpClass()
#		user = User(username='testcase', is_active=True, phone='1234567890', birthday='2016-01-01')
#		user.set_password('root')
#		user.save()
#		cls.user = user
		cls.client = Client()
		cls.factory = RequestFactory()

	def test_register_editor_normal(self):
		response = self.client.post('/auth/register/', {'username':'demo-editor', 'password':'demo-editor', 'confirm_password':'demo-editor', 'first_name':'demo editor firstname', 'last_name':'demo editor lastname', 'email':'tsengwoody.tw@gmail.com', 'phone':'1234567890', 'birthday':'2016-01-01', 'education':u'大學', 'role':'Editor', 'professional_field':u'資訊工程學'}, HTTP_X_REQUESTED_WITH='XMLHttpRequest', enforce_csrf_checks=True)
		self.assertEqual(response.status_code,200)
		self.assertEqual(len(Editor.objects.all()),1)
		self.assertEqual(len(User.objects.all()),1)
		editor = Editor.objects.first()
		self.assertEqual(editor.user.username, 'demo-editor')

	def test_register_editor_normal(self):
		response = self.client.post('/auth/register/', {'username':'demo-guest', 'password':'demo-guest', 'confirm_password':'demo-guest', 'first_name':'demo guest firstname', 'last_name':'demo guest lastname', 'email':'tsengwoody.tw@gmail.com', 'phone':'1234567890', 'birthday':'2016-01-01', 'education':u'大學', 'role':'Guest'}, HTTP_X_REQUESTED_WITH='XMLHttpRequest', enforce_csrf_checks=True)
		print response.content
		self.assertEqual(response.status_code,200)
		self.assertEqual(len(Guest.objects.all()),1)
		self.assertEqual(len(User.objects.all()),1)
		guest = Guest.objects.first()
		self.assertEqual(guest.user.username, 'demo-guest')

	@classmethod
	def tearDownClass(cls):
		super(registerTestCase, cls).tearDownClass()
