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
from ebookSystem.views import *
from genericUser.views import *
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
			is_supermanager=True,
			is_license = True,
			is_book = True,
			auth_email=True,
			auth_phone=True,
			education=u'學士',
		)
		root.set_password('eds@2018')
		root.status = root.STATUS['active']
		org = Organization.objects.create(name=u'eDocumentService', address=u'台北市大同區1段149號7樓', email=u'edocumentservice@gmail.com', phone='0917823098', is_service_center=True)
		root.org=org
		root.save()

		client = Client()
		client.login(username='root', password='eds@2018')
		previous_count = len(DisabilityCard.objects.all())
		response = client.post(
			reverse('genericUser:api:disabilitycard-list'),
			{
				"identity_card_number": "A129417526",
				"name": "曾奕勳",
				"address": "台北市大同區迪化街1段149號7樓",
				"identification_date": "2018-01-01",
				"renew_date": "2018-09-01",
				"level": "severe",
				"category": "vi",
				"owner": 1,
				'is_active': 'true',
			},
			HTTP_X_REQUESTED_WITH='XMLHttpRequest',
		)
		assert len(DisabilityCard.objects.all()) == previous_count +1, 'create announcement fail'

		pk = json.loads(response.content.decode('utf-8'))["identity_card_number"]
		dc = DisabilityCard.objects.get(identity_card_number=pk)
		dirname = os.path.dirname(dc.front)
		if not os.path.exists(dirname):
			os.makedirs(dirname, 755)
		shutil.copy2('temp/dcf.jpg', dc.front,)
		shutil.copy2('temp/dcb.jpg', dc.back,)


		client = Client()
		response = client.post(
			'/genericUser/api/users/',
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
				'is_editor': 'true',
				'is_book':'on',
				'org':u'1',
			}
		)
		print(response.content)
		editor = User.objects.get(username='demo-editor')
		editor.auth_email = True
		editor.auth_phone = True
		editor.save()
		assert editor.is_active == True, 'is_active False'
		assert editor.is_editor == True, 'is_editor False'
		assert editor.is_license == True, 'is_license False'

		with open('temp/dcf.jpg') as dcf_file, open('temp/dcb.jpg') as dcb_file:
			response = client.post(
			'/genericUser/api/users/',
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
					'is_guest':'true',
					'org':u'1',
				}
			)

		guest = User.objects.get(username='demo-guest')
		guest.auth_email = True
		guest.auth_phone = True
		guest.save()

		response = client.post(
			'/genericUser/api/users/',
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
				'is_editor':'true',
			},
		)

		manager = User.objects.get(username='demo-manager')
		manager.auth_email = True
		manager.auth_phone = True
		manager.save()

		category_instance = Category.objects.create(
			name='資訊工程學',
			org_id=org.id,
		)

		src = BASE_DIR +u'/temp/藍色駭客.zip'
		with open(src, 'rb') as book_file:
			client = Client()
			client.login(username='root', password='eds@2018')
			response = client.post(
				'/ebookSystem/api/books/action/create/',
				{
					u'ISBN': u'9789573321569',
					u'author': u'傑佛瑞.迪佛(Jeffery Deaver)著; 宋瑛堂譯',
					u'house': u'皇冠',
					u'bookname': u'藍色駭客',
					u'date': u'2005-07-01',
					u'bookbinding': '平裝',
					u'chinese_book_category': '874',
					u'order': '初版',
					'category_id': category_instance.id,
					'fileObject': book_file,
				},
				#HTTP_X_REQUESTED_WITH='XMLHttpRequest',
			)

		assert response.status_code == 202, 'status_code' +str(response.status_code) +str(response.content)
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
		client.login(username='root', password='eds@2018')
		response = client.post(
			'/ebookSystem/api/books/9789573321569/action/review/',
			{
				'result': 'success',
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
				edit_record = EditRecord.objects.get(part=ebook, number_of_times=ebook.number_of_times),
				user = User.objects.get(username='root'),
				time = timezone.now(),
				order = i,
				edit_count = count[i%5],
			)
		assert ebook.change_status(1, 'review'), 'change status error'


		ebook = EBook.objects.get(book=book, part=2)
		assert ebook.change_status(1, 'edit', user=root, deadline='2017-12-31'), 'change status error'
		ebook.service_hours = 80
		count = [0,0,1,2,3]
		for i in range(80):
			EditLog.objects.create(
				edit_record = EditRecord.objects.get(part=ebook, number_of_times=ebook.number_of_times),
				user = User.objects.get(username='root'),
				time = timezone.now(),
				order = i,
				edit_count = count[i%5],
			)
		assert ebook.change_status(1, 'review'), 'change status error'

		src = BASE_DIR +u'/temp/山羊島的藍色奇蹟.zip'
		with open(src, 'rb') as book_file:
			client = Client()
			client.login(username='root', password='eds@2018')
			response = client.post(
				'/ebookSystem/api/books/action/create/',
				{
					u'ISBN': u'9789866104626',
					u'author': u'多利安助川著; 卓惠娟譯',
					u'house': u'博識圖書',
					u'bookname': u'山羊島的藍色奇蹟',
					u'date': u'2015-07-01',
					u'bookbinding': '平裝',
					u'chinese_book_category': '861',
					u'order': '初版',
					'category_id': category_instance.id,
					'fileObject': book_file,
				},
#				HTTP_X_REQUESTED_WITH='XMLHttpRequest',
			)
		assert response.status_code == 202, 'status_code' +str(response.status_code)
		assert len(Book.objects.all())==2, 'create book fail'
		book = Book.objects.get(ISBN=u'9789866104626')
		assert os.path.exists(book.path), 'book resource folder not exist'
		assert len(EBook.objects.all()) == 16, 'create part fail'
		assert len(book.ebook_set.all())==6, 'create part fail'

		book_file = open(BASE_DIR +u'/temp/自創思維.epub', 'rb')
		client = Client()
		client.login(username='root', password='eds@2018')
		response = client.post(
			'/ebookSystem/api/books/action/upload/',
			{
				u'ISBN': u'9789863981459',
				u'author': u'雷德.霍夫曼(Reid Hoffman), 班.卡斯諾查(Ben Casnocha)著; 洪慧芳譯',
				u'house': u'天下雜誌',
				u'bookname': u'自創思維: 人生是永遠的測試版,瞬息萬變世界的新工作態度',
				u'date': u'2016-02-01',
				u'bookbinding': '平裝',
				u'chinese_book_category': '494',
				u'order': '第二版',
				'category_id': category_instance.id,
				'fileObject': book_file,
				'category': 'epub',
			},
#			HTTP_X_REQUESTED_WITH='XMLHttpRequest',
		)
		book_file.close()

		assert len(Book.objects.all())==3, 'create book fail'

		client = Client()
		client.login(username='root', password='eds@2018')
		previous_count = len(Announcement.objects.all())
		response = client.post(
			reverse(
				'genericUser:api:announcement-list'
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

		QAndA.objects.create(question='<p>question 1</p>', answer='<p>answer 1</p>', order=0)
		QAndA.objects.create(question='<p>question 2</p>', answer='<p>answer 2</p>', order=0)
		BannerContent.objects.create(
			title='我看不見書，但我想閱讀 - 雲端千眼',
			content='''
*	雲端千眼：我看不見書，但我想閱讀
	*	生活裡沒有書籍，就好像大地沒有陽光；智慧裡沒有書籍，就好像鳥兒沒有翅膀。
	*	我看不見書，但是我想閱讀。
	*	給視障者真正的閱讀權，需要各位加入共同參與，不限時地，只需透過網路，成為視障者雲端的眼。
	*	群眾參與，積砂成塔，邀請志工，期待你的加入。'''
			,
			order=0,
		)
		BannerContent.objects.create(
			title='我們可能無法做偉大的事，但可以用偉大的愛做小事 - 招募志工',
			content='''
*	加入我們：招募志工
	*	我們可能無法做偉大的事，但可以用偉大的愛做小事。
	*	We Want You, Apply Now.'''
			,
			order=1,
		)

		instance = ISSNBookInfo.objects.create(
			ISSN='16822811',
			title='科學人[中文版]',
			house='遠流出版事業股份有限公司',
		)
		ISSNBook.objects.create(
			ISSN_volume='16822811-3',
			ISSN_book_info=instance,
			volume='3',
			date='2018-01-01',
			owner=root,
		)

		client = Client()
		client.login(username='root', password='eds@2018')
		with open('temp/cover1.jpg', 'rb') as file:
			response = client.post(
				'/genericUser/api/bannercontents/1/resource/cover/image/',
				{
					'object': file,
				},
				HTTP_X_REQUESTED_WITH='XMLHttpRequest',
			)

		with open('temp/cover2.jpg', 'rb') as file:
			response = client.post(
				'/genericUser/api/bannercontents/2/resource/cover/image/',
				{
					'object': file,
				},
				HTTP_X_REQUESTED_WITH='XMLHttpRequest',
			)
