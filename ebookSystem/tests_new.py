# coding: utf-8
from django.test import TestCase, TransactionTestCase
# Create your tests here.

import shutil
import os
from django.core.urlresolvers import reverse
from django.test import Client, RequestFactory

from account.models import *
from ebookSystem.models import *
from guest.models import *
from genericUser.models import *
from .forms import *
from .tests_data import *

class downloadViewTests(TestCase):
	fixtures = ['dump.json',]

	def test_book_download_correct_case(self):
		client = Client()
		client.login(username='root', password='root')
		response = client.post(
			reverse(
				'ebookSystem:book_download',
				kwargs = {
					'ISBN': '9789863981459',
				},
			),
			{
				'password': 'root',
				'action': 'download',
			},
			HTTP_X_REQUESTED_WITH='XMLHttpRequest',
		)

	def test_ebook_download_correct_case(self):
		client = Client()
		client.login(username='root', password='root')
		response = client.post(
			reverse(
				'ebookSystem:ebook_download',
				kwargs = {
					'ISBN_part': '9789573321569-1',
				},
			),
			{
				'action': 'download',
				'password': 'root',
			},
			HTTP_X_REQUESTED_WITH='XMLHttpRequest',
		)

from django.core import mail
class message_sendViewTests(TestCase):
	fixtures = ['dump.json',]

	def test_message_send_correct_case1(self):
		client = Client()
		client.login(username='root', password='root')
		response = client.post(
			reverse(
				'ebookSystem:message_send',
			),
			{
				'action': 'editor_send',
				'subject': 'subject content',
				'body': 'body content',
			},
			HTTP_X_REQUESTED_WITH='XMLHttpRequest',
		)
		self.assertEqual(len(mail.outbox), 1)

	def test_message_send_correct_case2(self):
		client = Client()
		client.login(username='root', password='root')
		response = client.post(
			reverse(
				'ebookSystem:message_send',
			),
			{
				'action': 'guest_send',
				'subject': 'subject content',
				'body': 'body content',
			},
			HTTP_X_REQUESTED_WITH='XMLHttpRequest',
		)
		self.assertEqual(len(mail.outbox), 1)

class book_uploadViewTests(TestCase):
	fixtures = ['dump.json',]

	def test_upload_document_correct_case1(self):
		client = Client()
		client.login(username='root', password='root')
		previous_book_count = len(Book.objects.all())
		src = BASE_DIR +u'/temp/9789862621684.txt'
		book_file = open(src)
		data = BookInfo1_data.copy()
		data.update({
			'fileObject': book_file,
			'category': 'txt',
		})
		response = client.post(
			reverse(
				'ebookSystem:book_upload',
			),
			data,
			HTTP_X_REQUESTED_WITH='XMLHttpRequest',
		)
		book_file.close()
		self.assertEqual(len(Book.objects.all()), previous_book_count +1)
		book = Book.objects.get(ISBN='9789862621684')
		book.delete()

	def test_book_upload_repeat_case(self):
		client = Client()
		client.login(username='root', password='root')
		previous_book_count = len(Book.objects.all())
		src = BASE_DIR +u'/temp/藍色駭客.zip'
		book_file = open(src)
		data = BookInfo2_data.copy()
		data.update({
			'fileObject': book_file,
			'category': 'txt',
		})
		response = client.post(
			reverse(
				'ebookSystem:book_upload',
			),
			data,
			HTTP_X_REQUESTED_WITH='XMLHttpRequest',
		)
		book_file.close()
		self.assertEqual(len(Book.objects.all()), previous_book_count)

class book_createViewTests(TestCase):
	fixtures = ['dump.json',]

	def test_upload_document_correct_case(self):
		client = Client()
		client.login(username='root', password='root')
		previous_book_count = len(Book.objects.all())
		src = BASE_DIR +u'/temp/藍色駭客.zip'
		book_file = open(src)
		data = BookInfo2_data.copy()
		data.update({
			'fileObject': book_file,
		})
		response = client.post(
			reverse(
				'ebookSystem:book_create',
			),
			data,
			HTTP_X_REQUESTED_WITH='XMLHttpRequest',
		)
		book_file.close()
		self.assertEqual(len(Book.objects.all()), previous_book_count)

class book_deleteViewTests(TestCase):
	fixtures = ['dump.json',]
	def setUp(self):
		super(book_deleteViewTests, self).setUp()
		client = Client()
		client.login(username='root', password='root')

	def test_book_delete_correct_case1(self):
		client = Client()
		client.login(username='root', password='root')
		previous_book_count = len(Book.objects.all())
		src = BASE_DIR +u'/temp/羊與鋼之森.epub'
		book_file = open(src)
		data = BookInfo3_data.copy()
		data.update({
			'fileObject': book_file,
			'category': 'epub',
		})
		response = client.post(
			reverse(
				'ebookSystem:book_upload',
			),
			data,
			HTTP_X_REQUESTED_WITH='XMLHttpRequest',
		)
		book_file.close()
		book_count = len(Book.objects.all())
		self.assertEqual(book_count, previous_book_count +1)

		previous_book_count = len(Book.objects.all())

		path = Book.objects.get(ISBN=BookInfo3_data['ISBN']).path
		response = client.post(
			reverse(
				'ebookSystem:book_delete',
				kwargs = {
					'ISBN': BookInfo3_data['ISBN'],
				},
			),
			{
				'password': 'root',
			},
			HTTP_X_REQUESTED_WITH='XMLHttpRequest',
		)
		book_count = len(Book.objects.all())
		self.assertEqual(book_count, previous_book_count -1)
		self.assertEqual(os.path.exists(path), False)

	def test_book_delete_error_case1(self):
		client = Client()
		client.login(username='root', password='root')
		previous_book_count = len(Book.objects.all())
		response = client.post(
			reverse(
				'ebookSystem:book_delete',
				kwargs = {
					'ISBN': BookInfo2_data['ISBN'],
				},
			),
			{
				'password': 'root',
			},
			HTTP_X_REQUESTED_WITH='XMLHttpRequest',
		)
		self.assertEqual(len(Book.objects.all()), previous_book_count)

	def test_book_delete_error_case2(self):
		client = Client()
		client.login(username='root', password='root')
		previous_book_count = len(Book.objects.all())
		response = client.post(
			reverse(
				'ebookSystem:book_delete',
				kwargs = {
					'ISBN': BookInfo2_data['ISBN'],
				},
			),
			{
				'password': 'root1',
			},
			HTTP_X_REQUESTED_WITH='XMLHttpRequest',
		)
		self.assertEqual(len(Book.objects.all()), previous_book_count)

class book_listViewTests(TestCase):
	fixtures = ['dump.json',]
	def setUp(self):
		super(book_listViewTests, self).setUp()
		client = Client()
		client.login(username='root', password='root')

	def test_book_list_correct_case(self):
		client = Client()
		client.login(username='root', password='root')
		response = client.get(
			reverse(
				'ebookSystem:book_list',
			),
			{
				'query_type': 'chinese_book_category',
				'query_value': '8',
			},
			HTTP_X_REQUESTED_WITH='XMLHttpRequest',
		)
		import json
		for i in response.json()['content']['book']:
			print i

class book_listViewTests(TestCase):
	fixtures = ['dump.json',]
	def setUp(self):
		super(book_listViewTests, self).setUp()
		client = Client()
		client.login(username='root', password='root')

	def test_book_list_correct_case(self):
		client = Client()
		client.login(username='root', password='root')
		response = client.post(
			reverse(
				'ebookSystem:get_book_info_list',
			),
			{
				'FO_SearchField0': 'Title',
				'FO_SearchValue0': u'變態王子',
			},
			HTTP_X_REQUESTED_WITH='XMLHttpRequest',
		)
		print len(response.json()['bookinfo_list'])
