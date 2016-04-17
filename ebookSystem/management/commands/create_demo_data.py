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

class Command(BaseCommand):
	help = 'initial database'
	def add_arguments(self, parser):
		parser.add_argument('create_demo_data', nargs='*')

	def handle(self, *args, **options):
		root = User(username='root', email='tsengwoody.tw@gmail.com', first_name = 'demo root firstname', last_name = 'demo root lastname', is_active=True, is_superuser=True, is_staff=True, phone='1234567890', birthday='2016-01-01', is_scaner=True, is_manager=True, is_review=True)
		root.set_password('root')
		root.save()
		editor = User(username='demo-editor', email='tsengwoody.tw@gmail.com', first_name = 'demo editor firstname', last_name = 'demo editor lastname', is_active=True, phone='1234567890', birthday='2016-01-01')
		editor.set_password('demo-editor')
		editor.save()
		guest = User(username='demo-guest', email='tsengwoody.tw@gmail.com', first_name = 'demo guest firstname', last_name = 'demo guest lastname', is_active=True, phone='1234567890', birthday='2016-01-01', is_scaner=True)
		guest.set_password('demo-guest')
		guest.save()
		rootEditor = Editor.objects.create(user=root)
		rootGuest = Guest.objects.create(user=root)
		editorEditor = Editor.objects.create(user=editor)
		guestGuest = Guest.objects.create(user=guest)
		factory = RequestFactory()
		with open(u'temp/藍色駭客.zip') as fileObject:
			request = factory.post(reverse('guest:create_document'), {'bookname':u'藍色駭客', 'author':u'傑佛瑞．迪佛', 'translator':u'宋瑛堂', 'house':u'皇冠', 'ISBN':u'9573321564', 'date':u'2013-07-11', 'fileObject':fileObject, 'guest':'demo-guest'})
		request.user = root
		response = create_document(request)
		assert response.status_code == 200, 'response.status_code!=200'
		assert len(Book.objects.all())==1, 'create book fail'
		assert len(EBook.objects.all()) == 10, 'create part fail'
		book = Book.objects.get(ISBN=u'9573321564')
		book.is_active = True
		book.save()
		assert os.path.exists(book.path), 'book resource folder not exist'