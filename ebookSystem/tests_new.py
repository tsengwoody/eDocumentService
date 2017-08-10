# coding: utf-8
from django.test import TestCase
# Create your tests here.

import shutil
import os
from django.core.urlresolvers import reverse
from django.test import Client, RequestFactory

from account.models import *
from ebookSystem.models import *
from guest.models import *
from genericUser.models import *

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
			},
			HTTP_X_REQUESTED_WITH='XMLHttpRequest',
		)
		print response['Content-Disposition']

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
