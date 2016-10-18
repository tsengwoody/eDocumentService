# coding: utf-8
from django.core.management.base import BaseCommand, CommandError
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

from django.core.urlresolvers import reverse
from django.test import Client, RequestFactory
from django.utils import timezone

from account.models import *
from ebookSystem.models import *
from genericUser.models import *
from guest.models import *
from account.views import *
from ebookSystem.views import *
from genericUser.views import *
from mysite.views import register
from mysite.settings import BASE_DIR
import shutil

class Command(BaseCommand):
	help = 'initial database'
	def add_arguments(self, parser):
		parser.add_argument('create_demo_data', nargs='*')

	def handle(self, *args, **options):
		root = User(username='root', email='edocumentservice@gmail.com', first_name = 'demo root firstname', last_name = 'demo root lastname', is_active=True, is_superuser=True, is_staff=True, phone='0917823099', birthday='2016-01-01', is_editor=True, is_guest=True, is_manager=True, is_advanced_editor=True, status=User.STATUS['active'])
		root.set_password('root')
		root.save()
		rootEditor = Editor.objects.create(user=root)
		rootGuest = Guest.objects.create(user=root)
		factory = RequestFactory()
		request = factory.post(reverse('register'), {'username':'demo-editor', 'password':'demo-editor', 'email':'tsengwoody.tw@gmail.com', 'first_name':'demo editor firstname', 'last_name':'demo editor lastname', 'is_active':True, 'phone':'1234567890', 'birthday':'2016-01-01', 'education':u'碩士', 'editor':'Editor', 'professional_field':u'資訊工程學'})
		response = register(request)
		with open('temp/dcf.jpg') as dcf_file:
			with open('temp/dcb.jpg') as dcb_file:
				request = factory.post(reverse('register'), {'username':'demo-guest', 'password':'demo-guest', 'email':'tsengwoody.tw@gmail.com', 'first_name':'demo guest firstname', 'last_name':'demo guest lastname', 'is_active':True, 'phone':'1234567890', 'birthday':'2016-01-01', 'education':u'碩士', 'guest':'Guest', 'disability_card_front':dcf_file, 'disability_card_back':dcb_file})
				response = register(request)
				request = factory.post(reverse('register'), {'username':'demo-manager', 'password':'demo-manager', 'email':'tsengwoody.tw@gmail.com', 'first_name':'demo manager firstname', 'last_name':'demo manager lastname', 'is_active':True, 'phone':'1234567890', 'birthday':'2016-01-01', 'education':u'碩士', 'editor':'Editor', 'guest':'Guest', 'disability_card_front':dcf_file, 'disability_card_back':dcb_file, 'professional_field':u'資訊工程學'})
				response = register(request)
		manager = User.objects.get(username='demo-manager')
		manager.status = manager.STATUS['active']
		manager.is_editor=True
		manager.is_guest=True
		manager.is_manager=True
		manager.save()
		with open(u'temp/藍色駭客.zip') as fileObject:
			request = factory.post(reverse('genericUser:create_document'), {'bookname':u'藍色駭客', 'author':u'傑佛瑞．迪佛', 'house':u'皇冠', 'ISBN':u'9789573321569', 'date':u'2013-07-11', 'fileObject':fileObject})
		request.user = manager
		response = create_document(request)
		assert response.status_code == 302, 'status_code' +str(response.status_code)
		assert len(Book.objects.all())==1, 'create book fail'
		assert len(EBook.objects.all()) == 10, 'create part fail'
		book = Book.objects.get(ISBN=u'9789573321569')
		assert os.path.exists(book.path), 'book resource folder not exist'
		book.status = book.STATUS['active']
#		request = factory.post(reverse('account:profile'), {'getPart':''})
#		request.user = root
#		response = profileView.get(request)
		ebook = EBook.objects.get(book=book, part=1)
		ebook.edited_page = ebook.book.page_per_part -1
		ebook.editor = root
		ebook.get_date = timezone.now() -datetime.timedelta(days=30)
		ebook.deadline = ebook.get_date + datetime.timedelta(days=5)
		ebook.service_hours = 90
		ebook.group_ServiceHours()
		ebook.status = ebook.STATUS['finish']
		ebook.save()
		ebook = EBook.objects.get(book=book, part=2)
		ebook.edited_page = ebook.book.page_per_part -1
		ebook.editor = root
		ebook.get_date = timezone.now()
		ebook.deadline = ebook.get_date + datetime.timedelta(days=5)
		ebook.service_hours = 80
		ebook.sc_editor = root
		ebook.sc_get_date = timezone.now()
		ebook.sc_deadline = ebook.get_date + datetime.timedelta(days=5)
		ebook.sc_service_hours = 50
		ebook.group_ServiceHours()
		ebook.status=EBook.STATUS['sc_finish']
		ebook.save()
		from zipfile import ZipFile
		src = BASE_DIR +'/temp/part.zip'
		dst = ebook.book.path +u'/OCR'
		with ZipFile(src, 'r') as partFile:
			partFile.extractall(dst)
		request = factory.post(reverse('genericUser:apply_document'), {u'ISBN':u'9789865829810', u'bookname':u'遠山的回音', u'author':u'卡勒德.胡賽尼(Khaled Hosseini)著; 李靜宜譯', u'house':u'木馬文化', u'date':u'2014-02-01'})
		request.user = manager
		response = apply_document(request)
		org = Organization.objects.create(name=u'eDocumentService', address=u'台北市大同區1段149號7樓', email=u'edocumentservice@gmail.com', phone='0917823099', manager=root, is_service_center=True)
		root.org=org
		root.save()
		article = Article.objects.create(author=root, subject=u'平台操作說明', category=u'文件')
		src = BASE_DIR +'/temp/article_NVDA.zip'
		dst = BASE_DIR +'/static/article/{0}'.format(article.id)
		with ZipFile(src, 'r') as partFile:
			partFile.extractall(dst)
		assert len(ApplyDocumentAction.objects.all()) == 1, 'create ApplyDocumentAction fail'