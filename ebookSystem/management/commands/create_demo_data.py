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
		root = User(username='root', email='edocumentservice@gmail.com', first_name = 'demo root firstname', last_name = 'demo root lastname', is_active=True, is_superuser=True, is_staff=True, phone='0917823099', birthday='2016-01-01', is_editor=True, is_guest=True, is_manager=True, is_advanced_editor=True, education=u'學士')
		root.set_password('root')
		root.status = root.STATUS['active']
		root.auth_email = True
		root.auth_phone = True
		root.auth_privacy = True
		root.save()
		rootEditor = Editor.objects.create(user=root, professional_field=u'資訊工程學')
		rootGuest = Guest.objects.create(user=root)
		factory = RequestFactory()
		request = factory.post(reverse('register'), {'username':'demo-editor', 'password':'demo-editor', 'email':'tsengwoody.tw@gmail.com', 'first_name':'demo editor firstname', 'last_name':'demo editor lastname', 'is_active':True, 'phone':'1234567890', 'birthday':'2016-01-01', 'education':u'碩士', 'role':'Editor', 'professional_field':u'資訊工程學','is_privacy':True})
		response = register(request)
		#print "-------regiest demo_editor-------"
		with open('temp/dcf.jpg') as dcf_file:
			with open('temp/dcb.jpg') as dcb_file:
				request = factory.post(reverse('register'), {'username':'demo-guest', 'password':'demo-guest', 'email':'tsengwoody.tw@gmail.com', 'first_name':'demo guest firstname', 'last_name':'demo guest lastname', 'is_active':True, 'phone':'1234567890', 'birthday':'2016-01-01', 'education':u'碩士', 'role':'Guest', 'disability_card_front':dcf_file, 'disability_card_back':dcb_file,'is_privacy':True})
				response = register(request)
				request = factory.post(reverse('register'), {'username':'demo-manager', 'password':'demo-manager', 'email':'tsengwoody.tw@gmail.com', 'first_name':'demo manager firstname', 'last_name':'demo manager lastname', 'is_active':True, 'phone':'1234567890', 'birthday':'2016-01-01', 'education':u'碩士', 'role':'Editor', 'professional_field':u'資訊工程學','is_privacy':True})
				response = register(request)
		manager = User.objects.get(username='demo-manager')
		manager.status = manager.STATUS['active']
		manager.is_editor=True
		manager.is_guest=True
		manager.is_manager=True
		manager.save()
		src = BASE_DIR +u'/temp/藍色駭客.zip'
		with open(src) as fileObject:
			request = factory.post(reverse('genericUser:create_document'), {'bookname':u'藍色駭客', 'author':u'傑佛瑞．迪佛', 'house':u'皇冠', 'ISBN':u'9789573321569', 'date':u'2013-07-11', 'fileObject':fileObject})
		request.user = root
		response = create_document(request)
		assert response.status_code == 302, 'status_code' +str(response.status_code)
		assert len(Book.objects.all())==1, 'create book fail'
		book = Book.objects.get(ISBN=u'9789573321569')
		assert os.path.exists(book.path), 'book resource folder not exist'
		from zipfile import ZipFile
		src = BASE_DIR +'/temp/part.zip'
		dst = book.path +u'/OCR'
		with ZipFile(src, 'r') as partFile:
			partFile.extractall(dst)
		book.status = book.STATUS['active']
		book.save()
		book.create_EBook()
		assert len(EBook.objects.all()) == 10, 'create part fail'
		ebook = EBook.objects.get(book=book, part=1)
		assert ebook.change_status(1, 'active'), 'change status error'
		assert ebook.change_status(1, 'edit', user=root), 'change status error'
		assert ebook.change_status(1, 'review'), 'change status error'
		assert ebook.change_status(1, 'finish'), 'change status error'
		ebook.service_hours = 90
		ebook.group_ServiceHours()
		ebook.save()
		ebook = EBook.objects.get(book=book, part=2)
		assert ebook.change_status(1, 'active'), 'change status error'
		assert ebook.change_status(1, 'edit', user=root), 'change status error'
		assert ebook.change_status(1, 'review'), 'change status error'
		assert ebook.change_status(1, 'finish'), 'change status error'
		ebook.service_hours = 80
		assert ebook.change_status(1, 'sc_edit', user=root), 'change status error'
		assert ebook.change_status(1, 'sc_finish'), 'change status error'
		ebook.sc_service_hours = 50
		ebook.group_ServiceHours()
		ebook.save()

		src = BASE_DIR +u'/temp/山羊島的藍色奇蹟.zip'
		with open(src) as fileObject:
			request = factory.post(reverse('genericUser:create_document'), {'bookname':u'山羊島的藍色奇蹟', 'author':u'多利安助川著; 卓惠娟譯', 'house':u'博識圖書', 'ISBN':u'9789866104626', 'date':u'2015-07-01', 'fileObject':fileObject})
		request.user = root
		response = create_document(request)
		assert response.status_code == 302, 'status_code' +str(response.status_code)
		assert len(Book.objects.all())==2, 'create book fail'
		book = Book.objects.get(ISBN=u'9789866104626')
		assert os.path.exists(book.path), 'book resource folder not exist'
		url = reverse('ebookSystem:review_document', kwargs={'book_ISBN':9789866104626})
		request = factory.post(url, {u'reason': [u''], u'page': [u'0'], u'scanPageList': [u'A00001.jpg'], u'review': [u'success']})
		request.user = root
		response = review_document(request, u'9789866104626')
		assert len(EBook.objects.all()) == 16, 'create part fail'
		assert len(book.ebook_set.all())==6, 'create part fail'
		src = BASE_DIR +'/temp/part-finish.zip'
		dst = book.path +u'/OCR'
		with ZipFile(src, 'r') as partFile:
			partFile.extractall(dst)
		for ebook in book.ebook_set.all():
			assert ebook.change_status(1, 'edit', user=root), 'change status error'
			assert ebook.change_status(1, 'review'), 'change status error'
			assert ebook.change_status(1, 'finish'), 'change status error'
			ebook.service_hours = 80
			ebook.group_ServiceHours()
			ebook.save()

		request = factory.post(reverse('genericUser:apply_document'), {u'ISBN':u'9789865829810', u'bookname':u'遠山的回音', u'author':u'卡勒德.胡賽尼(Khaled Hosseini)著; 李靜宜譯', u'house':u'木馬文化', u'date':u'2014-02-01'})
		request.user = manager
		response = apply_document(request)
		org = Organization.objects.create(name=u'eDocumentService', address=u'台北市大同區1段149號7樓', email=u'edocumentservice@gmail.com', phone='0917823099', manager=root, is_service_center=True)
		root.org=org
		root.save()
		src = BASE_DIR +'/temp/article_NVDA.zip'
		with open(src) as fileObject:
			request = factory.post(reverse('genericUser:article/create'), {u'subject':u'NVDA使用者手冊', u'category':u'文件', u'zipFile':fileObject })
		request.user = root
		response = article_create(request)
		assert len(Article.objects.all()) == 1, 'create Article fail'
		assert len(ApplyDocumentAction.objects.all()) == 1, 'create ApplyDocumentAction fail'