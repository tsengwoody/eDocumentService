# coding: utf-8
from django.test import TestCase, TransactionTestCase
# Create your tests here.

from django.contrib.auth import authenticate
from django.core.urlresolvers import reverse
from django.test import Client, RequestFactory

from .models import *
from .forms import *

class UserViewTests(TestCase):
	fixtures = ['dump.json',]

	def test_user_view_correct_case(self):
		client = Client()
		client.login(username='root', password='root')
#		previous_count = len(QAndA.objects.all())
		response = client.get(
			reverse(
				'genericUser:user_view',
				kwargs = {
					'ID': '1',
				}
			),
			{
				'action': 'disability_card',
			},
			HTTP_X_REQUESTED_WITH='XMLHttpRequest',
		)
		print len(response.json()['content'])

	def test_user_update_correct_case(self):
		client = Client()
		client.login(username='root', password='root')
		src = BASE_DIR +u'/temp/dcb.jpg'
		back_file = open(src)
		src = BASE_DIR +u'/temp/dcf.jpg'
		front_file = open(src)
		response = client.post(
			reverse(
				'genericUser:user_update',
				kwargs = {
					'ID': '1',
				}
			),
			{
				'action': 'disability_card',
				'front': front_file,
				'back': back_file,
			},
			HTTP_X_REQUESTED_WITH='XMLHttpRequest',
		)
