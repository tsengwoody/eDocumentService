# coding: utf-8
from django.contrib import messages
from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseServerError 
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import generic
from ebookSystem.models import *
from .models import *
from .forms import *
from utils.decorator import *
from utils.validate import *
from mysite.settings import SERVICE
import json
import os
import shutil


@http_response
def userGuide(request, template_name='home.html'):
#	logger.info('{}/home\t{}'.format(resolve(request.path).namespace, request.user))
	return render(request, template_name, locals())

@view_permission
@http_response
def book_repository(request, template_name='guest/book_repository.html'):
	edit_book_list = request.user.own_book_set.all().filter(status__lte=Book.STATUS['review'])
	finish_book_list = request.user.own_book_set.all().filter(status__gte=Book.STATUS['finish'])
	bookinfos = [ book.book_info for book in finish_book_list ]
	if request.method == 'POST':
		print request.POST
		if request.POST.has_key('email'):
			from django.core.mail import EmailMessage
			getBook = Book.objects.get(ISBN=request.POST['email'])
			attach_file_path = getBook.zip(request.user, request.POST['password'])
			if not attach_file_path:
				status = 'error'
				message = u'準備文件失敗'
				return locals()
			subject = u'[文件] {0}'.format(getBook)
			body = u'新愛的{0}您好：\n'.format(request.user.username)
			email = EmailMessage(subject=subject, body=body, from_email=SERVICE, to=[request.user.email])
			email.attach_file(attach_file_path)
			email.send(fail_silently=False)
			status = 'success'
			message = u'已寄送到您的電子信箱'
			os.remove(attach_file_path)
		if request.POST.has_key('download'):
			getBook = Book.objects.get(ISBN=request.POST['download'])
			attach_file_path = getBook.zip(request.user, request.POST['password'])
			if not attach_file_path:
				status = 'error'
				message = u'準備文件失敗'
				return locals()
			download_path = attach_file_path
			download_filename = os.path.basename(attach_file_path)
		if request.POST.has_key('delete'):
			deleteBook = Book.objects.get(ISBN=request.POST['delete'])
			deleteBook.delete()
			status = 'success'
			message = u'成功刪除文件'
		edit_book_list = request.user.own_book_set.all().filter(status__lte=Book.STATUS['review'])
		finish_book_list = request.user.own_book_set.all().filter(status__gte=Book.STATUS['finish'])
		return locals()
	if request.method == 'GET':
		return locals()
