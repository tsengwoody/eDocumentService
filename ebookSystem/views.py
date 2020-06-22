# coding: utf-8
import base64
import json
import os
import uuid

from django.core.cache import cache
from django.shortcuts import render
from .models import *

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

def generics(request, name, pk=None):
	template_name='ebookSystem/{0}.html'.format(name.split('/')[0])
	return render(request, template_name, {})

def library_view(request, template_name='ebookSystem/library_view.html'):
	if request.method == 'GET':
		if not request.user.is_guest:
			return render(request, template_name, locals())
		lr = LibraryRecord.objects.get(id=request.GET['ISBN'])

		token = uuid.uuid4().hex
		# cache.set('token.' +str(request.user.id), token, 100)
		path = '/library_epub/' +str(lr.id) +'/' +token + '.epub'
		path = path.encode('ascii')
		#path = '/ebookSystem/api/libraryrecords/{0}/resource/source/epub'.format(str(lr.id))
		base64_path = base64.b64encode(path).decode('ascii')
	return render(request, template_name, locals())

def library_origin_view(request, template_name='ebookSystem/library_origin_view.html'):
	if request.method == 'GET':
		if not request.user.is_guest:
			status = 'error'
			message = ''
			return render(request, template_name, locals())
		book = Book.objects.get(ISBN=request.GET['ISBN'])
		if not (book.status == 5 and book.source != 'self'):
			book.realtime_epub_create()

		token = uuid.uuid4().hex
		# cache.set('token.' +str(request.user.id), token, 10)
		path = '/library_origin_epub/' +book.ISBN +'/' +token +'.epub'
		path = path.encode('ascii')
		base64_path = base64.b64encode(path).decode('ascii')
	return render(request, template_name, locals())
