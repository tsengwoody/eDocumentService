# coding: utf-8
import codecs
import datetime
import base64
from zipfile import ZipFile
from django.core.cache import cache
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse, resolve
from django.db.models import F,Q
from django.forms import modelform_factory
from django.http import HttpResponseRedirect,HttpResponse, Http404
from django.shortcuts import render
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import generic
from .models import *
from .forms import *
from genericUser.models import Event
from mysite.settings import BASE_DIR, SERVICE
from utils.analysis import *
from utils.crawler import *
from utils.decorator import *
from utils.uploadFile import handle_uploaded_file
from utils.resource import *
import os
import json
import shutil
import uuid
from django.views.decorators.cache import cache_control

#logging config
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
# create file handler
fh = logging.FileHandler(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'log') +'/views.log')
fh.setLevel(logging.DEBUG)
# create formatter
formatter = logging.Formatter('%(asctime)s\t%(name)s\t%(levelname)s\t%(message)s')
# add formatter to fh
fh.setFormatter(formatter)
# add ch to logger
logger.addHandler(fh)

@http_response
def generics(request, name, pk=None):
	template_name='ebookSystem/{0}.html'.format(name.split('/')[0])
	return locals()

@http_response
def mathml(request, template_name='ebookSystem/editor.html'):
	if request.method == 'POST':
		if request.POST.has_key('set'):
			cache.set(request.user.username, {'mathml':request.POST['content']}, 600)
			status = u'success'
			message = u'成功暫存內容'
		if request.POST.has_key('get'):
			if not cache.has_key(request.user.username):
				status = u'error'
				message = u'server無資料'
				return locals()
			math_content = cache.get(request.user.username)['mathml']
			extra_list = ['math_content']
			status = u'success'
			message = u'成功獲取內容'
		return locals()
	if request.method == 'GET':
		status = u'success'
		message = u'成功獲取內容'
		return locals()

@user_category_check(['manager'])
@http_response
def review_document(request, book_ISBN, template_name='ebookSystem/review_document.html'):
	try:
		book = Book.objects.get(ISBN=book_ISBN)
	except:
		raise Http404("book does not exist")
	events = Event.objects.filter(content_type__model='book', object_id=book.ISBN, status=Event.STATUS['review'])

	if request.method == 'GET':
		return locals()

	if request.method == 'POST':
		if request.POST['review'] == 'success':
			for part in book.ebook_set.all():
				part.change_status(1, 'active', category='based')
				BookOrder.refresh()
			status = 'success'
			message = u'審核通過文件'
			for event in events:
				event.response(status=status, message=message, user=request.user)
		if request.POST['review'] == 'error':
			book.delete()
			status = 'success'
			message = u'審核退回文件'
			for event in events:
				event.response(status='error', message=request.POST['reason'], user=request.user)
		redirect_to = reverse('manager:event_list', kwargs={'action':'book' })
		return locals()

@http_response
def detail(request, book_ISBN, template_name='ebookSystem/detail.html'):
	users = User.objects.all()
	try:
		book = Book.objects.get(ISBN=book_ISBN)
	except:
		raise Http404("book does not exist")
	if request.method == 'POST':
		if request.POST.has_key('email'):
			from django.core.mail import EmailMessage
			getPart = EBook.objects.get(ISBN_part=request.POST['email'])
			attach_file_path = getPart.zip(request.user, request.POST['password'])
			if not attach_file_path:
				status = 'error'
				message = u'準備文件失敗'
				return locals()
			subject = u'[文件] {0}'.format(getPart)
			body = u'新愛的{0}您好：\n'.format(request.user.username)
			email = EmailMessage(subject=subject, body=body, from_email=SERVICE, to=[request.user.email])
			email.attach_file(attach_file_path)
			email.send(fail_silently=False)
			status = 'success'
			message = u'已寄送到您的電子信箱'
			os.remove(attach_file_path)
		elif request.POST.has_key('assign'):
			getPart = EBook.objects.get(ISBN_part=request.POST['assign'])
			user = User.objects.get(username=request.POST['username'])
			deadline = request.POST['deadline'].split('-')
			deadline = [ int(v) for v in deadline ]
			deadline = timezone.datetime(deadline[0], deadline[1], deadline[2])
			getPart.change_status(1, 'edit', user=user, deadline=deadline)
			status = u'success'
			message = u'指派校對成功'
		return locals()
	if request.method == 'GET':
		return locals()

@user_category_check(['manager'])
@http_response
def detail_manager(request, book_ISBN, template_name='ebookSystem/detail_manager.html'):
	try:
		book = Book.objects.get(ISBN=book_ISBN)
	except:
		raise Http404("book does not exist")
	if request.method == 'POST':
		if request.POST.has_key('upload'):
			getPart = EBook.objects.get(ISBN_part=request.POST['upload'])
			uploadFilePath = os.path.join(getPart.book.path, '{0}.zip'.format(getPart.ISBN_part))
			with open(uploadFilePath, 'wb+') as dst:
				for chunk in request.FILES['fileObject'].chunks():
					dst.write(chunk)
			try:
				with ZipFile(uploadFilePath, 'r') as uploadFile:
					uploadFile.testzip()
					uploadFile.extractall(getPart.book.path +'/OCR')
			except BaseException as e:
				print e
				os.remove(uploadFilePath)
				status = 'error'
				message = u'非正確ZIP文件'
				return locals()
			os.remove(uploadFilePath)
		elif request.POST.has_key('reset'):
			getPart = EBook.objects.get(ISBN_part=request.POST['reset'])
			getPart.add_tag()
			with codecs.open(getPart.get_path('-finish'), 'w', encoding='utf-8') as finishFile:
				finishFile.write(u'\ufeff')
		return locals()
	if request.method == 'GET':
		return locals()

@http_response
def book_info(request, ISBN, template_name='ebookSystem/book_info.html'):
	ISBN = request.POST['ISBN']
	if len(ISBN) == 10 and not ISBN10_check(ISBN):
		status = u'error'
		message = u'ISBN10碼錯誤'
		return locals()
	if len(ISBN) == 13 and not ISBN13_check(ISBN):
		status = u'error'
		message = u'ISBN13碼錯誤'
		return locals()
	if len(ISBN) == 10:
		ISBN = ISBN10_to_ISBN13(ISBN)

	if request.POST['source'] == 'NCL':
		#=====NCL=====
		try:
			[ISBN, bookname, author, house, date, bookbinding, chinese_book_category, order] = get_ncl_bookinfo(ISBN)
			source = 'NCL'
		except BaseException as e:
			status = 'error'
			message = u'查無資料'
			return locals()

	elif request.POST['source'] == 'douban':
		#=====douban=====
		try:
			[ISBN, bookname, author, house, date, bookbinding,] = get_douban_bookinfo(ISBN)
			chinese_book_category, order = ('', '')
			source = 'douban'
		except BaseException as e:
			status = 'error'
			message = u'查無資料'
			return locals()

	status = 'success'
	message = u'成功取得資料'
	extra_list = ['bookname', 'author', 'house', 'date', 'ISBN', 'bookbinding', 'chinese_book_category', 'order', 'source']
	return locals()

@http_response
def get_book_info_list(request, template_name='ebookSystem/book_info.html'):
	if request.method == 'POST' and request.is_ajax():

		if request.POST['source'] == 'NCL':

			p_logic = re.compile(r'FO_SchRe1ation(?P<count>\d+)')
			p_field = re.compile(r'FO_SearchField(?P<count>\d+)')
			p_value = re.compile(r'FO_SearchValue(?P<count>\d+)')

			query_dict = {}
			for k,v in request.POST.iteritems():
				search_logic = p_logic.search(k)
				search_field = p_field.search(k)
				search_value = p_value.search(k)
				if search_logic or search_field or search_value:
					query_dict[k] = v

			try:
				bookinfo_list = get_ncl_bookinfo_list(query_dict)
				source = 'NCL'
			except BaseException as e:
				status = 'error'
				message = u'查詢書籍錯誤。{0}'.format(unicode(e))
				return locals()

		elif request.POST['source'] == 'douban':
			try:
				bookinfo_list = get_douban_bookinfo_list(request.POST['search_query'])
				source = 'douban'
			except BaseException as e:
				status = 'error'
				message = u'查詢書籍錯誤。{0}'.format(unicode(e))
				return locals()

		status = 'success'
		if len(bookinfo_list) >0:
			message = u'查無指定書籍'
		else:
			message = u'查詢書籍成功'
		extra_list = ['bookinfo_list', 'source']
		return locals()


def edit_ajax(request, ISBN_part, *args, **kwargs):
	print request.POST
	user = request.user
	response = {}
	if not getattr(request.user, 'is_editor', None):
		response['status'] = u'error'
		response['message'] = u'已登出'
	if not request.POST.has_key('online'):
		response['status'] = 'error'
		response['message'] = ''
		return HttpResponse(json.dumps(response), content_type="application/json")
	delta = timezone.now() - user.online
	if delta.seconds < 50:
		response['status'] = u'error'
		response['message'] = u'您有其他編輯正進行'
		return HttpResponse(json.dumps(response), content_type="application/json")
	user.online = timezone.now()
	user.save()
	part = EBook.objects.get(ISBN_part=ISBN_part)
	part.service_hours = part.service_hours+1
	part.save()

	editRecord = EditRecord.objects.get(part=part, number_of_times=part.number_of_times)

	order = len(EditLog.objects.filter(edit_record=editRecord))
	EditLog.objects.create(edit_record=editRecord, user=request.user, time=timezone.now(), order=order, edit_count=int(request.POST['online']))
	response['status'] = u'success'
	response['message'] = part.service_hours
	return HttpResponse(json.dumps(response), content_type="application/json")

@cache_control(no_store=True, no_cache=True, max_age=0)
@http_response
def edit(request, template_name='ebookSystem/edit.html', encoding='utf-8', *args, **kwargs):
	try:
		part = EBook.objects.get(ISBN_part=kwargs['ISBN_part'])
	except: 
		raise Http404("book or part does not exist")

	if request.method == 'GET':
		return locals()

@http_response
def full_edit(request, ISBN_part, template_name='ebookSystem/full_edit.html'):
	try:
		part = EBook.objects.get(ISBN_part=ISBN_part)
	except:
		raise Http404("book does not exist")
	[scanPageList, defaultPageURL] = part.get_org_image(request.user)
	editContent = part.get_content('-sc')
	if request.method == 'POST':
		with codecs.open(part.get_path('-sc'), 'w', encoding='utf-8') as scFile:
			scFile.write(u'\ufeff' +request.POST['content'])
		return locals()
	if request.method == 'GET':
		return locals()

#==========
@user_category_check(['guest'])
@http_response
def book_download(request, ISBN, ):
	if request.method == 'POST' and request.is_ajax():
		if not request.user.is_guest:
				status = 'error'
				message = u'取得文件失敗：您並非視障者權限'
				return locals()

		DOWNLOAD_MIN_DURATION_TIME = 86400
		MIN_DURATION_TIME = 86400
		getBook = Book.objects.get(ISBN=ISBN)
		gbr = GetBookRecord.objects.filter(book=getBook, user=request.user)
#		if len(gbr) <= 0:
		if not getBook.owner == request.user and len(gbr) <= 0:
			try:
				allow_download = cache.get(request.user.username)['get_book']
				status = 'error'
				message = u'取得文件失敗：1天內僅能下載1本新書，下次可下載的時間為{0}'.format(timezone.localtime(allow_download))
				return locals()
			except BaseException as e:
				pass

		#準備所需文件
		try:
			attach_file_path = getBook.zip(request.user, request.POST['password'], request.POST['format'])
		except BaseException as e:
			status = 'error'
			message = u'準備文件失敗：{0}'.format(unicode(e))
			return locals()

		if request.POST['action'] == 'download':
			download_path = attach_file_path
			download_filename = os.path.basename(attach_file_path)
		elif request.POST['action'] == 'email':
			subject = u'[文件] {0}'.format(getBook)
			body = u'新愛的{0}您好：\n'.format(request.user.username)
			email = EmailMessage(subject=subject, body=body, from_email=SERVICE, to=[request.user.email])
			email.attach_file(attach_file_path)
			email.send(fail_silently=False)
			status = 'success'
			message = u'已寄送到您的電子信箱'

		from utils.other import get_client_ip
		get_ip = get_client_ip(request)
		GetBookRecord.objects.create(book=getBook, user=request.user, get_ip=get_ip)
		'''if len(gbr) <= 0:
			cache.set(request.user.username, {'get_book': timezone.now() +datetime.timedelta(seconds=MIN_DURATION_TIME)}, MIN_DURATION_TIME)
		else:
			pass'''

		return locals()

@http_response
def ebook_download(request, ISBN_part, ):
	if request.method == 'POST' and request.is_ajax():
		getPart = EBook.objects.get(ISBN_part=ISBN_part)
		try:
			if request.POST['action'] == 'view':
				attach_file_path = getPart.get_clean_file()
			elif request.POST['action'] == 'view_se':
				attach_file_path = getPart.get_clean_file()
				attach_file_path = getPart.replace()
			elif request.POST['action'] == 'download_full':
				attach_file_path = getPart.zip_full()
			elif request.POST['action'] == 'download':
				attach_file_path = getPart.zip(request.user, request.POST['password'])
			else:
				attach_file_path = None
		except BaseException as e:
			status = 'error'
			message = u'準備文件失敗'
			return locals()
		download_path = attach_file_path
		download_filename = os.path.basename(attach_file_path)
		return locals()

@http_response
def message_send(request, template_name='ebookSystem/message_send.html', ):
	if request.method == 'POST' and request.is_ajax():
		from django.core.mail import EmailMessage
		if request.POST['action'] == 'editor_send':
			user_email_list = [ i.email for i in User.objects.filter(is_editor=True) if i.is_book and i.auth_email ]
		if request.POST['action'] == 'guest_send':
			user_email_list = [ i.email for i in User.objects.filter(is_guest=True) if i.is_book and i.auth_email ]
		subject = request.POST['subject']
		body = request.POST['body']
		email = EmailMessage(subject=subject, body=body, from_email=SERVICE, to=[SERVICE], bcc=user_email_list)
		email.send(fail_silently=False)
		status = 'success'
		message = u'訊息傳送成功'
		return locals()
	if request.method == 'GET':
		return locals()

from django.contrib.auth import authenticate
@user_category_check(['manager'])
@http_response
def book_delete(request):
	if request.method == 'POST' and request.is_ajax():
		getBook = Book.objects.get(ISBN=request.POST['ISBN'])
		try:
			user = authenticate(username=request.user.username, password=request.POST['password'])
			if user is None:
				raise SystemError(u'使用者驗證失敗')
			if not getBook.owner == user and not user.is_manager:
				raise SystemError(u'非擁有者無法刪除')
			if getBook.source == 'self' and getBook.status > getBook.STATUS['inactive']:
				raise SystemError(u'校對書籍無法刪除')
			getBook.delete()
		except BaseException as e:
			status = 'error'
			message = u'文件刪除失敗: {0}'.format(unicode(e))
			return locals()
		status = 'success'
		message = u'文件刪除成功: finish'
		return locals()

@http_response
def book_action(request):
	if request.method == 'POST' and request.is_ajax():
		getBook = Book.objects.get(ISBN=request.POST['ISBN'])
		try:
			user = authenticate(username=request.user.username, password=request.POST['password'])
			if user is None:
				raise SystemError(u'使用者驗證失敗')

			if request.POST['action'] == 'set_priority':
				if not (int(request.POST['priority']) > 0 and int(request.POST['priority']) < 10):
					raise SystemError(u'權重數值錯誤，請輸入0-9之數值')
				getBook.priority = int(request.POST['priority'])
				getBook.save()

		except BaseException as e:
			status = 'error'
			message = u'book {0}: error'.format(request.POST['action'])
			return locals()
		status = 'success'
		message = u'book {0}: success'.format(request.POST['action'])
		return locals()

@http_response
def getbookrecord_user(request, ID, template_name='ebookSystem/getbookrecord_user.html'):
	user = User.objects.filter(id=ID)
	gbr_list = GetBookRecord.objects.filter(user=user)
	if request.method == 'GET':
		return locals()

import mimetypes
import os
from django.http import FileResponse, Http404, HttpResponse, HttpResponseNotModified

def epub(request, ISBN):
	book = Book.objects.get(ISBN=ISBN)
#	fullpath = book.path +'/OCR/{0}.epub'.format(book.ISBN)
	fullpath = '/django/eDocumentService/file/ebookSystem/document/9789863981459/OCR/9789863981459.epub'

	statobj = os.stat(fullpath)
	content_type, encoding = mimetypes.guess_type(fullpath)
	content_type = content_type or 'application/octet-stream'
	response = FileResponse(open(fullpath, 'rb'), content_type=content_type)
#	response["Last-Modified"] = http_date(statobj.st_mtime)
#	if stat.S_ISREG(statobj.st_mode):
#		response["Content-Length"] = statobj.st_size
	if encoding:
		response["Content-Encoding"] = encoding
	return response

@http_response
def library_view(request, template_name='ebookSystem/library_view.html'):
	if request.method == 'GET':
		if not request.user.is_guest:
			status = 'error'
			message = ''
			return locals()
		lr = LibraryRecord.objects.get(id=request.GET['ISBN'])

		token = uuid.uuid4().hex
		cache.set('token.' +str(request.user.id), token, 100)
		path = '/library_epub/' +str(lr.id) +'/' +token
		base64_path = base64.b64encode(path)
		return locals()

@http_response
def library_origin_view(request, template_name='ebookSystem/library_origin_view.html'):
	if request.method == 'GET':
		if not request.user.is_guest:
			status = 'error'
			message = ''
			return locals()
		book = Book.objects.get(ISBN=request.GET['ISBN'])
		if not book.status == book.STATUS['final']:
			final_epub = book.path +'/OCR/{0}.epub'.format(book.ISBN)
			try:
				part_list = [ file.get_clean_file() for file in book.ebook_set.all() ]
				from utils.epub import html2epub
				info = {
					'ISBN': book.book_info.ISBN,
					'bookname': book.book_info.bookname,
					'author': book.book_info.author,
					'date': str(book.book_info.date),
					'house': book.book_info.house,
					'language': 'zh',
				}
				html2epub(part_list, final_epub, **info)
			except BaseException as e:
				raise SystemError('epub create fail (not final):' +unicode(e))

		token = uuid.uuid4().hex
		cache.set('token.' +str(request.user.id), token, 10)
		path = '/library_origin_epub/' +book.ISBN +'/' +token
		base64_path = base64.b64encode(path)
		return locals()

@http_response
def library_action(request, ):
	if request.method == 'POST' and request.is_ajax():
		if request.POST['action'] == 'check_out':
			book = Book.objects.get(ISBN=request.POST['ISBN'])
			lr_user = request.user.libraryrecord_set.filter(status=True)
			if len(lr_user) >5:
				status = 'error'
				message = u'已到達借閱上限，同時可借閱書量為5本，請先歸還書籍再借閱'
				return locals()
			if len(lr_user.filter(object=book)) >0:
				status = 'error'
				message = u'已在借閱書櫃無需再借閱'
				return locals()
			lr = LibraryRecord.objects.create(user=request.user, object=book)
			lr = LibraryRecord.objects.get(id=lr.id)
			lr.check_out()
			status = 'success'
			message = u'成功借閱書籍{0}'.format(book)
		elif request.POST['action'] == 'check_in':
			lr = LibraryRecord.objects.get(id=request.POST['id'])
			lr.check_in()
			status = 'success'
			message = u'成功歸還書籍{0}'.format(lr.object)
		return locals()


@http_response
def bookorder_list(request, template_name='ebookSystem/bookorder_list.html'):
	bookorder_list = BookOrder.objects.all().order_by('order')
	if request.method == 'GET':
		return locals()

#=====file=====
from django.http import Http404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from genericUser.premissions import IsManager

@api_view(['POST',])
def ebook_change_status(request, pk):
	try:
		ebook = EBook.objects.get(ISBN_part=pk)
	except EBook.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)
	if request.method == 'POST':
		try:
			user = User.objects.get(id=request.POST['user_id'])
		except:
			user = None
		try:
			deadline = request.POST['deadline'].split('-')
			deadline = [ int(v) for v in deadline ]
			deadline = timezone.datetime(deadline[0], deadline[1], deadline[2])
		except:
			deadline = None

		direction = int(request.POST['direction'])
		try:
			ebook.change_status(direction=direction, status=request.POST['status'], user=user, deadline=deadline)
		except BaseException as e:
			raise e
			return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
		return Response(status=status.HTTP_202_ACCEPTED)
