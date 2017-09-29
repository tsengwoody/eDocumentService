# coding: utf-8
from django.test import TestCase, TransactionTestCase
# Create your tests here.

from django.contrib.auth import authenticate
from django.core.urlresolvers import reverse
from django.test import Client, RequestFactory

from .models import *
from .forms import *

class AnnouncementViewTests(TestCase):
	fixtures = ['dump.json',]

	def test_announcement_create_correct_case(self):
		client = Client()
		client.login(username='root', password='root')
		previous_count = len(Announcement.objects.all())
		response = client.post(
			reverse(
				'genericUser:announcement_create',
			),
			{
				'title': u'title',
				'content': u'<p>content_p1</p><p>content_p2</p>',
				'category': u'志工快訊',
			},
			HTTP_X_REQUESTED_WITH='XMLHttpRequest',
		)
		self.assertEqual(len(Announcement.objects.all()), previous_count+1)

	def test_announcement_update_correct_case(self):
		client = Client()
		client.login(username='root', password='root')
		announcement = Announcement.objects.get(id=1)
		response = client.post(
			reverse(
				'genericUser:announcement_update',
				kwargs = {
					'id': announcement.id,
				},
			),
			{
				'title': u'title',
				'content': u'<p>content_p1</p><p>content_p2</p><p>content_p3</p>',
				'category': u'志工快訊',
			},
			HTTP_X_REQUESTED_WITH='XMLHttpRequest',
		)
		announcement = Announcement.objects.get(id=1)
		self.assertEqual(announcement.content, u'<p>content_p1</p><p>content_p2</p><p>content_p3</p>')
