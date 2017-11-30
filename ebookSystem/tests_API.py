# coding: utf-8
from django.test import TestCase, TransactionTestCase
# Create your tests here.

from django.core.urlresolvers import reverse
from django.test import Client, RequestFactory

from ebookSystem.models import *
from genericUser.models import *
from .forms import *
from .tests_data import *

class EBookAPITests(TestCase):
	fixtures = ['dump.json',]

	def test_ebook_cl_case(self):
		client = Client()
		client.login(username='root', password='root')
		response = client.get(
			reverse(
				'ebookSystem:ebook-list',
			),
			HTTP_X_REQUESTED_WITH='XMLHttpRequest',
		)
		print response.status_code
		print len(response.json())

class BookAPITests(TestCase):
	fixtures = ['dump.json',]

	def test_book_rud_case(self):
		client = Client()
		client.login(username='root', password='root')
		response = client.get(
			reverse(
				'ebookSystem:book-detail',
				kwargs = {
					'pk': u'9789573321569',
				}
			),
			HTTP_X_REQUESTED_WITH='XMLHttpRequest',
		)
		print response.status_code
		print response.json()['owners']
		print response.json()['owner']
