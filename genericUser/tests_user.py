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
#		self.assertEqual(len(QAndA.objects.all()), previous_count+1)

	def test_qanda_update_correct_case(self):
		client = Client()
		client.login(username='root', password='root')
		qanda = QAndA.objects.get(id=1)
		response = client.post(
			reverse(
				'genericUser:qanda_update',
				kwargs = {
					'id': qanda.id,
				},
			),
			{
				'question': '<p>question update</p>',
				'answer': '<p>answer update</p>',
			},
			HTTP_X_REQUESTED_WITH='XMLHttpRequest',
		)
		qanda = QAndA.objects.get(id=1)
		self.assertEqual(qanda.question, '<p>question update</p>')

	def test_qanda_list_correct_case(self):
		client = Client()
		client.login(username='root', password='root')
		qanda_list = [i.serialized() for i in QAndA.objects.all()]
		response = client.get(
			reverse(
				'genericUser:qanda_list',
			),
			HTTP_X_REQUESTED_WITH='XMLHttpRequest',
		)
		self.assertEqual(response.json()['content'], qanda_list)
