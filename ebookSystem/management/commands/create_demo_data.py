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
from genericUser.views import create_document, revise_content, apply_document
from mysite.views import register

class Command(BaseCommand):
	help = 'initial database'
	def add_arguments(self, parser):
		parser.add_argument('create_demo_data', nargs='*')

	def handle(self, *args, **options):
		root = User(username='root', email='edocumentservice@gmail.com', first_name = 'demo root firstname', last_name = 'demo root lastname', is_active=True, is_superuser=True, is_staff=True, phone='0917823099', birthday='2016-01-01', is_editor=True, is_guest=True, is_manager=True, status=ACTIVE)
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
		manager.status = ACTIVE
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
		request = factory.post(reverse('genericUser:revise_content'), {'book_ISBN':'9789573321569', 'part':'1', 'content':'<p>附近傳來響亮的電子哀叫聲。紀列德被嚇了一跳。片刻後才認出這聲響，是他在聖妓從沒聽過的聲音。法蘭克﹒畢修普接聽手機。骨瘦憔悴的他聆聽一會兒，撥弄著一邊鬢須，然後回答:『是的，隊長其他呢?』他停頓良久，嘴角略微緊縮。『你沒辦法嗎……好吧，隊長。』</p>\r\n<p>他掛掉電話。</p>\r\n<p>安德森對他揚起一邊眉毛。命案科的警探畢修普口氣平穩地說:『剛才是班斯亭隊長。梅林三屍搶案又有新的進展。有人在胡桃溪附近看見歹徒，也許往我們的方向逃逸。』他快速瞥了紀列德一眼，彷佛他是長椅上的汙潰，然後對安德森說:『我應該告訴你，我講上級把我從這</p>'})
		request.user = manager
		response = revise_content(request)
		assert len(ReviseContentAction.objects.all()) == 1, 'create ReviseContentAction fail'
		request = factory.post(reverse('genericUser:apply_document'), {u'ISBN':u'9789865829810', u'bookname':u'遠山的回音', u'author':u'卡勒德.胡賽尼(Khaled Hosseini)著; 李靜宜譯', u'house':u'木馬文化', u'date':u'2014-02-01'})
		request.user = manager
		response = apply_document(request)
		assert len(ApplyDocumentAction.objects.all()) == 1, 'create ApplyDocumentAction fail'