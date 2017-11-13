# coding: utf-8
from django.core.management.base import BaseCommand, CommandError
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

from django.core.urlresolvers import reverse
from django.test import Client, RequestFactory
from django.utils import timezone

from ebookSystem.models import *
from genericUser.models import *
from account.views import *
from ebookSystem.views import *
from genericUser.views import *
from mysite.views import register
from mysite.settings import BASE_DIR
import shutil
import datetime

class Command(BaseCommand):
	help = 'initial database'
	def add_arguments(self, parser):
		parser.add_argument('create_demo_data', nargs='*')

	def handle(self, *args, **options):
		root = User(
			username='root',
			email='edocumentservice@gmail.com',
			first_name = 'demo root firstname',
			last_name = 'demo root lastname',
			is_active=True,
			is_superuser=True,
			is_staff=True,
			phone='0917823099',
			birthday='2016-01-01',
			is_editor=True,
			is_guest=True,
			is_manager=True,
			is_advanced_editor=True,
			is_license = True,
			is_book = True,
			auth_email=True,
			auth_phone=True,
			education=u'學士',
		)
		root.set_password('root')
		root.status = root.STATUS['active']
		root.save()
		org = Organization.objects.create(name=u'eDocumentService', address=u'台北市大同區1段149號7樓', email=u'edocumentservice@gmail.com', phone='0917823098', manager=root, is_service_center=True)
		root.org=org
		root.save()

		client = Client()
		response = client.post(
			reverse('register'),
			{
				'username':'demo-editor',
				'password':'demo-editor',
				'confirm_password':'demo-editor',
				'email':'tsengwoody.tw@gmail.com',
				'first_name':'demo editor firstname',
				'last_name':'demo editor lastname',
				'phone':'1234567890',
				'birthday':'2016-01-01',
				'education':u'碩士',
				'role':'Editor',
				'is_book':'on',
				'org':u'1',
				'professional_field':u'資訊工程學',
				'is_privacy':True
			}
		)

		client = Client()
		response = client.post(
			reverse(
				'genericUser:review_user',
				kwargs = {
					'username': 'demo-editor',
				},
			),
			{
				'active': 'on',
				'editor': 'on',
#				'guest': 'on',
				'review': 'success',
				'reason': '',
			},
		)

		editor = User.objects.get(username='demo-editor')
		editor.auth_email = True
		editor.auth_phone = True
		editor.save()
		assert editor.is_active == True, 'is_active False'
		assert editor.is_editor == True, 'is_editor False'
		assert editor.is_license == True, 'is_license False'

		with open('temp/dcf.jpg') as dcf_file, open('temp/dcb.jpg') as dcb_file:
			response = client.post(
				reverse('register'),
				{
					'username':'demo-guest',
					'password':'demo-guest',
					'confirm_password':'demo-guest',
					'email':'tsengwoody@gmail.com',
					'first_name':'demo guest firstname',
					'last_name':'demo guest lastname',
					'phone':'1234567899',
					'birthday':'2016-01-01',
					'education':u'碩士',
					'is_book':'on',
					'role':'Guest',
					'org':u'1',
					'disability_card_front':dcf_file,
					'disability_card_back':dcb_file,
					'is_privacy':True,
				}
			)

		response = client.post(
			reverse(
				'genericUser:review_user',
				kwargs = {
					'username': 'demo-guest',
				},
			),
			{
				'active': 'on',
#				'editor': 'on',
				'guest': 'on',
				'review': 'success',
				'reason': '',
			},
		)

		guest = User.objects.get(username='demo-guest')
		guest.auth_email = True
		guest.auth_phone = True
		guest.save()

		response = client.post(
			reverse('register'),
			{
				'username':'demo-manager',
				'password':'demo-manager',
				'confirm_password':'demo-manager',
				'email':'tsengwoody@yahoo.com.tw',
				'first_name':'demo manager firstname',
				'last_name':'demo manager lastname',
				'phone':'1234567898',
				'birthday':'2016-01-01',
				'education':u'碩士',
				'is_book':'on',
				'org':u'1',
				'role':'Editor',
				'professional_field':u'資訊工程學',
				'is_privacy':True,
			},
		)

		response = client.post(
			reverse(
				'genericUser:review_user',
				kwargs = {
					'username': 'demo-manager',
				},
			),
			{
				'active': 'on',
				'editor': 'on',
				'manager': 'on',
				'review': 'success',
				'reason': '',
			},
		)

		manager = User.objects.get(username='demo-manager')
		manager.auth_email = True
		manager.auth_phone = True
		manager.save()

		src = BASE_DIR +u'/temp/藍色駭客.zip'
		with open(src) as book_file:
			client = Client()
			client.login(username='root', password='root')
			response = client.post(
				reverse(
					'ebookSystem:book_create'
				),
				{
					u'ISBN': u'9789573321569',
					u'author': u'傑佛瑞.迪佛(Jeffery Deaver)著; 宋瑛堂譯',
					u'house': u'皇冠',
					u'bookname': u'藍色駭客',
					u'date': u'2005-07-01',
					u'bookbinding': '平裝',
					u'chinese_book_category': '874',
					u'order': '初版',
					'fileObject': book_file,
				},
#				HTTP_X_REQUESTED_WITH='XMLHttpRequest',
			)

#		print response.json()['message']
		assert response.status_code == 302, 'status_code' +str(response.status_code)
		assert len(Book.objects.all())==1, 'create book fail'
		assert len(EBook.objects.all()) == 10, 'create part fail'

		book = Book.objects.get(ISBN='9789573321569')
		assert os.path.exists(book.path), 'book resource folder not exist'

		from zipfile import ZipFile
		src = BASE_DIR +'/temp/part.zip'
		dst = book.path +u'/OCR'
		with ZipFile(src, 'r') as partFile:
			partFile.extractall(dst)

		client = Client()
		client.login(username='root', password='root')
		response = client.post(
			reverse(
				'ebookSystem:review_document',
				kwargs = {
					'book_ISBN': '9789573321569',
				},
			),
			{
				'review': 'success',
				'reason': '',
			},
			HTTP_X_REQUESTED_WITH='XMLHttpRequest',
		)

		ebook = EBook.objects.get(book=book, part=1)
		assert ebook.change_status(1, 'edit', user=root, deadline='2017-12-31'), 'change status error'
		ebook.service_hours = 90
		ebook.save()
		count = [0,0,1,2,3]
		for i in range(90):
			EditLog.objects.create(
				edit_record = EditRecord.objects.get(part=ebook, category='based', number_of_times=ebook.number_of_times),
				user = User.objects.get(username='root'),
				time = timezone.now(),
				order = i,
				edit_count = count[i%5],
			)
		assert ebook.change_status(1, 'review'), 'change status error'
		src = BASE_DIR +u'/temp/part1-finish-sp.txt'
		shutil.copy2(src, ebook.get_path('-finish'))
		client = Client()
		client.login(username='root', password='root')
		response = client.post(
			reverse(
				'ebookSystem:review_part',
				kwargs = {
					'ISBN_part': ebook.ISBN_part,
				},
			),
			{
				'review': 'success',
				'reason': '',
			},
			HTTP_X_REQUESTED_WITH='XMLHttpRequest',
		)

		ebook = EBook.objects.get(book=book, part=2)
		assert ebook.change_status(1, 'edit', user=root, deadline='2017-12-31'), 'change status error'
		ebook.service_hours = 80
		count = [0,0,1,2,3]
		for i in range(80):
			EditLog.objects.create(
				edit_record = EditRecord.objects.get(part=ebook, category='based', number_of_times=ebook.number_of_times),
				user = User.objects.get(username='root'),
				time = timezone.now(),
				order = i,
				edit_count = count[i%5],
			)
		assert ebook.change_status(1, 'review'), 'change status error'
		src = BASE_DIR +u'/temp/part1-finish-sp.txt'
		shutil.copy2(src, ebook.get_path('-finish'))
		client = Client()
		client.login(username='root', password='root')
		response = client.post(
			reverse(
				'ebookSystem:review_part',
				kwargs = {
					'ISBN_part': ebook.ISBN_part,
				},
			),
			{
				'review': 'success',
				'reason': '',
			},
			HTTP_X_REQUESTED_WITH='XMLHttpRequest',
		)

		src = BASE_DIR +u'/temp/山羊島的藍色奇蹟.zip'
		with open(src) as book_file:
			client = Client()
			client.login(username='root', password='root')
			response = client.post(
				reverse('ebookSystem:book_create'),
				{
					u'ISBN': u'9789866104626',
					u'author': u'多利安助川著; 卓惠娟譯',
					u'house': u'博識圖書',
					u'bookname': u'山羊島的藍色奇蹟',
					u'date': u'2015-07-01',
					u'bookbinding': '平裝',
					u'chinese_book_category': '861',
					u'order': '初版',
					'fileObject': book_file,
				},
#				HTTP_X_REQUESTED_WITH='XMLHttpRequest',
			)
		assert response.status_code == 302, 'status_code' +str(response.status_code)
		assert len(Book.objects.all())==2, 'create book fail'
		book = Book.objects.get(ISBN=u'9789866104626')
		assert os.path.exists(book.path), 'book resource folder not exist'
		assert len(EBook.objects.all()) == 16, 'create part fail'
		assert len(book.ebook_set.all())==6, 'create part fail'

		book_file = open(BASE_DIR +u'/temp/自創思維.epub')
		client = Client()
		client.login(username='root', password='root')
		response = client.post(
			reverse(
				'ebookSystem:book_upload'
			),
			{
				u'ISBN': u'9789863981459',
				u'author': u'雷德.霍夫曼(Reid Hoffman), 班.卡斯諾查(Ben Casnocha)著; 洪慧芳譯',
				u'house': u'天下雜誌',
				u'bookname': u'自創思維: 人生是永遠的測試版,瞬息萬變世界的新工作態度',
				u'date': u'2016-02-01',
				u'bookbinding': '平裝',
				u'chinese_book_category': '494',
				u'order': '第二版',
				'fileObject': book_file,
				'category': 'epub',
			},
#			HTTP_X_REQUESTED_WITH='XMLHttpRequest',
		)
		book_file.close()
		assert len(Book.objects.all())==3, 'create book fail'

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
		assert len(Announcement.objects.all()) == previous_count +1, 'create announcement fail'
		GetBookRecord.objects.create(book=book, user=root, get_ip='192.168.1.0')
		GetBookRecord.objects.create(book=book, user=root, get_ip='192.168.1.0')

		QAndA.objects.create(question='<p>question 1</p>', answer='<p>answer 1</p>', )
		QAndA.objects.create(question='<p>question 2</p>', answer='<p>answer 2</p>', )

		client = Client()
		client.login(username='root', password='root')
		previous_count = len(LibraryRecord.objects.all())
		response = client.post(
			reverse(
				'ebookSystem:library_action'
			),
			{
				'ISBN': '9789863981459',
				'action': 'check_out',
			},
			HTTP_X_REQUESTED_WITH='XMLHttpRequest',
		)
		assert len(LibraryRecord.objects.all()) == previous_count +1, 'create announcement fail'
