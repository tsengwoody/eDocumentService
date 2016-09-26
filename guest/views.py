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

class profileView(generic.View):
	template_name=''

	@method_decorator(user_category_check(['guest']))
	@method_decorator(http_response)
	def get(self, request, *args, **kwargs):
		template_name=self.template_name
		edit_book_list = request.user.own_book_set.all().exclude(status__lte=EBook.STATUS['review'])
		finish_book_list = request.user.own_book_set.all().exclude(status__gte=EBook.STATUS['finish'])
		return locals()

	@method_decorator(user_category_check(['guest']))
	@method_decorator(http_response)
	def post(self, request, *args, **kwargs):
		template_name=self.template_name
		if request.POST.has_key('emailBook'):
			from django.core.mail import EmailMessage
			book_ISBN = request.POST.get('emailBook')
			emailBook = Book.objects.get(ISBN = book_ISBN)
			subject = u'[文件] {}'.format(emailBook.book_info.bookname)
			body = u'新愛的{0}您好：\n'.format(request.user.username)
			email = EmailMessage(subject=subject, body=body, from_email=SERVICE, to=[request.user.email])
			attach_file_path = emailBook.zip('test')
			if attach_file_path == '':
				status = 'error'
				message = u'附加文件失敗'
				os.remove(attach_file_path)
				return locals()
			email.attach_file(attach_file_path)
			email.send(fail_silently=False)
			status = 'success'
			message = u'已寄送到您的電子信箱'
			os.remove(attach_file_path)
#		if request.POST.has_key('delete'):
#			book_ISBN = request.POST.get('delete')
#			deleteBook = Book.objects.get(ISBN = book_ISBN)
#			deletePath = deleteBook.path
#			shutil.rmtree(deletePath)
#			deleteBook.delete()
#			status = 'success'
#			message = u'成功刪除文件'
		edit_book_list = request.user.own_book_set.all().exclude(status__lte=EBook.STATUS['review'])
		finish_book_list = request.user.own_book_set.all().exclude(status__gte=EBook.STATUS['finish'])
		return locals()
