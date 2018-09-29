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
from mysite.settings import BASE_DIR, SERVICE
from utils.decorator import *
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

def edit_ajax(request, ISBN_part, *args, **kwargs):
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

#==========


from django.contrib.auth import authenticate

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
		#path = '/ebookSystem/api/libraryrecords/{0}/resource/source/epub'.format(str(lr.id))
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
