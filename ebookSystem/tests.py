# coding: utf-8
from django.test import TestCase
# Create your tests here.

import shutil
import os
from django.core.urlresolvers import reverse
from django.test import Client, RequestFactory

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

class detailViewTests(baseViewTests):
	def setUp(self):
		super(detailViewTests, self).setUp()
		src = BASE_DIR +u'/temp/藍色駭客.zip'
		with open(src) as book_file:
			client = Client()
			client.login(username='root', password='root')
			response = client.post(
				reverse(
					'genericUser:create_document'
				),
{
				u'ISBN': u'9789573321568',
				u'author': u'傑佛瑞.迪佛(Jeffery Deaver)著; 宋瑛堂譯',
				u'house': u'皇冠',
				u'bookname': u'藍色駭客',
				u'date': u'2005-07-01',
				u'bookbinding': '平裝',
				u'chinese_book_category': '874',
				u'order': '初版',
				'fileObject': book_file,
			},
#				HTTP_X_REQUESTED_WITH='XMLHttpRequest',
			)
		response = client.post(
			reverse(
				'ebookSystem:review_document',
				kwargs = {
					'book_ISBN': '9789573321568',
				},
			),
			{
				'review': 'success',
				'reason': '',
			},
			HTTP_X_REQUESTED_WITH='XMLHttpRequest',
		)

	'''def test_detail_correct_case(self):
		response = self.client.post(
			reverse(
				'ebookSystem:detail',
				kwargs = {
					'book_ISBN': '9789573321568',
				},
			),
			{
				u'assign': u'9789573321568-1',
				u'username': u'root',
				u'deadline': u'2017-07-15',
			}
		)
		ebook = EBook.objects.get(ISBN_part='9789573321568-1')
		self.assertEqual(ebook.status, 2)
		self.assertEqual(ebook.editor.username, 'root')
		print ebook.deadline'''

	def test_search_correct_case(self):
		response = self.client.post(
			reverse(
				'ebookSystem:search_book',
			),
			{
				'search_type' :'ISBN',
				'search_value': '9789573321568',
			},
			HTTP_X_REQUESTED_WITH='XMLHttpRequest',
		)
		print response.json()['content']

	def tearDown(self):
		super(detailViewTests, self).tearDown()
		try:
			book = Book.objects.get(ISBN='9789573321568')
			shutil.rmtree(book.path)
		except BaseException as e:
			print(e)
