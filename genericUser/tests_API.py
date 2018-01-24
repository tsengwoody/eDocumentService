﻿# coding: utf-8
from django.test import TestCase, TransactionTestCase
# Create your tests here.

from django.core.urlresolvers import reverse
from django.test import Client, RequestFactory

from ebookSystem.models import *
from genericUser.models import *
from .forms import *
from .tests_data import *

import json

class UserAPITests(TestCase):
	fixtures = ['dump.json',]

	def test_user_cl_case(self):
		client = Client()
		client.login(username='root', password='root')
		response = client.post(
			reverse(
				'genericUser:api:user-list',
			),
			{
				'username':'demo-editor-test',
				'email':'tsengwoody.tw@gmail.com',
				'first_name':'demo editor firstname',
				'last_name':'demo editor lastname',
				'phone':'1234567890',
				'birthday':'2016-01-01',
				'education':u'碩士',
				'is_book':'on',
				'org':u'1',
			'is_license':True,
				'is_editor':True,
				'is_guest':False,
			'is_advanced_editor':False,
			'auth_email':False,
			'auth_phone':False,
				'password':'demo-editor',
				'confirm_password':'demo-editor',
			},
			HTTP_X_REQUESTED_WITH='XMLHttpRequest',
		)
		pk = json.loads(response.content.decode('utf-8'))['id']
		instance = User.objects.get(id=pk)
		from django.contrib.auth import authenticate
		user = authenticate(username=instance.username, password='demo-editor')
		print user.id

	def test_user_set_password_case(self):
		client = Client()
		client.login(username='root', password='root')
		response = client.post(
			reverse(
				'genericUser:api:user-set-password',
				kwargs = {
					'pk': 1,
				}
			),
			{
				'old_password':'root',
				'new_password1':'new',
				'new_password2':'new',
			},
			HTTP_X_REQUESTED_WITH='XMLHttpRequest',
		)
		pk = 1
		instance = User.objects.get(id=pk)
		from django.contrib.auth import authenticate
		user = authenticate(username=instance.username, password='new')
		print user
