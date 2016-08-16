# coding: utf-8
from django.core.management.base import BaseCommand, CommandError
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

from django.core.urlresolvers import reverse
from django.test import Client, RequestFactory


from account.models import *
from ebookSystem.models import *
from genericUser.models import *
from guest.models import *
from guest.views import create_document
from mysite.views import register

class Command(BaseCommand):
	help = 'initial database'
#	def add_arguments(self, parser):
#		parser.add_argument('create_demo_data', nargs='*')

	def handle(self, *args, **options):
		root = User(username='root', email='edocumentservice@gmail.com', first_name = 'demo root firstname', last_name = 'demo root lastname', is_active=True, is_superuser=True, is_staff=True, phone='0917823099', birthday='2016-01-01', is_editor=True, is_guest=True, is_manager=True, is_advanced_editor=True, status=ACTIVE)
		root.set_password('root')
		root.save()
		rootEditor = Editor.objects.create(user=root)
		rootGuest = Guest.objects.create(user=root)
'''		factory = RequestFactory()
		with open('temp/dcf.jpg') as dcf_file:
			with open('temp/dcb.jpg') as dcb_file:
				request = factory.post(reverse('register'), {'username':'tony', 'password':'tony', 'email':'tony_tseng@pchome.com.tw', 'first_name':u'曾', 'last_name':u'孟崎', 'is_active':True, 'phone':'0920415077', 'birthday':'1956-02-17', 'education':u'大學', 'editor':'Editor', 'guest':'Guest', 'disability_card_front':dcf_file, 'disability_card_back':dcb_file, 'professional_field':u''})
				response = register(request)
		manager = User.objects.get(username='tony')
		manager.status = ACTIVE
		manager.is_editor=True
		manager.is_guest=True
		manager.is_manager=True
		manager.is_advanced_editor=True
		manager.save()'''