# coding: utf-8
from django.test import TestCase, TransactionTestCase
# Create your tests here.

from django.core.urlresolvers import reverse
from django.test import Client, RequestFactory

from ebookSystem.models import *
from genericUser.models import *
from .tests_data import *

class EBookResourceTests(TestCase):
	fixtures = ['dump.json',]

	def test_ebook_resource_post_case(self):
		src = BASE_DIR +u'/temp/9789862621684.txt'
		file_object = open(src)
		client = Client()
		client.login(username='root', password='root')
		response = client.post(
			reverse(
				'ebookSystem:resource:ebook-resource',
				kwargs = {
					'pk': '9789866104626-3',
					'dir': 'OCR',
					'resource': 'sc',
				},
			),
			{
				'object': file_object,
				},
			HTTP_X_REQUESTED_WITH='XMLHttpRequest',
		)
		print response.status_code
