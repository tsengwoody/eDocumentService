# coding: utf-8
from django.test import TestCase, TransactionTestCase
# Create your tests here.

from django.contrib.auth import authenticate
from django.core.urlresolvers import reverse
from django.test import Client, RequestFactory

from .models import *
from .forms import *

class user_updateViewTests(TestCase):
	fixtures = ['dump.json',]

	def test_user_update_action_info_correct_case(self):
		client = Client()
		client.login(username='root', password='root')
		user = User.objects.get(id=1)
		response = client.post(
			reverse(
				'genericUser:user_update',
				kwargs = {
					'ID': user.id,
				},
			),
			{
				'action': 'info',
				'username': user.username,
				'first_name': user.first_name,
				'last_name': user.last_name,
				'email': 'edocumentserviceu@gmail.com',
				'phone': '0912345678',
				'birthday': '2017-01-22',
				'education': u'碩士',
				'is_book':'False',
				'org':u'1',
			},
			HTTP_X_REQUESTED_WITH='XMLHttpRequest',
		)
		user = User.objects.get(id=1)
		self.assertEqual(user.email, 'edocumentserviceu@gmail.com')

	def test_user_update_action_password_correct_case(self):
		client = Client()
		client.login(username='root', password='root')
		user = User.objects.get(id=1)
		response = client.post(
			reverse(
				'genericUser:user_update',
				kwargs = {
					'ID': user.id,
				},
			),
			{
				'action': 'password',
				'old_password': 'root',
				'new_password1': 'root1',
				'new_password2': 'root1',
			},
			HTTP_X_REQUESTED_WITH='XMLHttpRequest',
		)
		user = User.objects.get(id=1)
		user_auth = authenticate(username=user.username, password='root1')
		self.assertEqual(user, user_auth)

	def test_user_update_action_role_correct_case(self):
		client = Client()
		client.login(username='root', password='root')
		user = User.objects.get(id=1)
		response = client.post(
			reverse(
				'genericUser:user_update',
				kwargs = {
					'ID': user.id,
				},
			),
			{
				'action': 'role',
				'is_editor': 'True',
			},
			HTTP_X_REQUESTED_WITH='XMLHttpRequest',
		)
		user = User.objects.get(id=1)
		self.assertEqual(user.is_editor, True)

class user_viewViewTests(TestCase):
	fixtures = ['dump.json',]

	def test_correct_case(self):
		client = Client()
		client.login(username='root', password='root')
		user = User.objects.get(id=1)
		response = client.post(
			reverse(
				'genericUser:user_update',
				kwargs = {
					'ID': user.id,
				},
			),
			{
				'action': 'info',
			},
			HTTP_X_REQUESTED_WITH='XMLHttpRequest',
		)
#		self.assertEqual(		response.json()['content']['user'], user.serialized())

	def test_user_update_action_password_correct_case(self):
		client = Client()
		client.login(username='root', password='root')
		user = User.objects.get(id=1)
		response = client.post(
			reverse(
				'genericUser:user_update',
				kwargs = {
					'ID': user.id,
				},
			),
			{
				'action': 'password',
				'old_password': 'root',
				'new_password1': 'root1',
				'new_password2': 'root1',
			},
			HTTP_X_REQUESTED_WITH='XMLHttpRequest',
		)
		user = User.objects.get(id=1)
		user_auth = authenticate(username=user.username, password='root1')
		self.assertEqual(user, user_auth)

	def test_user_update_action_role_correct_case(self):
		client = Client()
		client.login(username='root', password='root')
		user = User.objects.get(id=1)
		response = client.post(
			reverse(
				'genericUser:user_update',
				kwargs = {
					'ID': user.id,
				},
			),
			{
				'action': 'role',
				'is_editor': 'True',
			},
			HTTP_X_REQUESTED_WITH='XMLHttpRequest',
		)
		user = User.objects.get(id=1)
		self.assertEqual(user.is_editor, True)

class announcement_createViewTests(TestCase):
	fixtures = ['dump.json',]

	def test_announcement_create_correct_case(self):
		client = Client()
		client.login(username='root', password='root')
		previous_count = len(Announcement.objects.all())
		response = client.post(
			reverse(
				'genericUser:announcement_create'
			),
			{
				'title': u'title',
				'content': u'<p>content_p1</p><p>content_p2</p>',
				'category': u'志工快訊',
			},
			HTTP_X_REQUESTED_WITH='XMLHttpRequest',
		)
		self.assertEqual(len(Announcement.objects.all()), previous_count +1)

class user_listViewTests(TestCase):
	fixtures = ['dump.json',]

	def test_announcement_create_correct_case(self):
		client = Client()
		client.login(username='root', password='root')
		response = client.get(
			reverse(
				'genericUser:user_list'
			),
			{
				'action': 'role',
				'query_field': 'all',
			},
			HTTP_X_REQUESTED_WITH='XMLHttpRequest',
		)
#		print response.json()['content'][0]
#		self.assertEqual()
