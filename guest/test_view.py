# coding: utf-8
from django.core.urlresolvers import reverse
from django.http import HttpRequest,HttpResponse
from django.test import Client, RequestFactory, TestCase
from account.models import Editor
from ebookSystem.models import *
from genericUser.models import User
from guest.models import Guest
from guest.views import *
from mysite import settings
import os
import shutil

class create_documentTestCase(TestCase):
	@classmethod
	def setUpClass(cls):
		super(create_documentTestCase, cls).setUpClass()
		user = User(username='testcase', is_active=True, phone='1234567890', birthday='2016-01-01')
		user.set_password('root')
		user.save()
		guest = Guest(user=user)
		guest.save()
		cls.user = user
		cls.factory = RequestFactory()

	def test_create_document(self):
		with open('temp/uploadTestFile.zip') as fileObject:
			request = self.factory.post(reverse('guest:create_document'), {'bookname':u'遠山的回音test2','author':u'Khaled Hosseini','translator':u'李靜宜','house':u'木馬文化','ISBN':u'9789865829810','date':u'2014-01-22', 'fileObject': fileObject})
		request.user = self.user
		response = create_document(request)
		self.assertEqual(response.status_code,200)
		self.assertEqual(len(Book.objects.all()),1)
		self.assertEqual(len(EBook.objects.all()),4)
		book =Book.objects.first()
		self.assertTrue(os.path.exists(book.path))
		shutil.rmtree(book.path)

	@classmethod
	def tearDownClass(cls):
		super(create_documentTestCase, cls).tearDownClass()