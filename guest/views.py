# coding: utf-8
from django.contrib import messages
from django.core.cache import cache
from django.core.mail import EmailMessage
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
import json
import shutil

class profileView(generic.View):
	template_name=''

	@method_decorator(user_category_check(['guest']))
	@method_decorator(http_response)
	def get(self, request, *args, **kwargs):
		readme_url = request.path +'readme/'
		template_name=self.template_name
		user=request.user
		book_list = user.guest.own_book_set.all()
		edit_book_list = user.guest.own_book_set.all().exclude(status=Book.STATUS['edit'])
		finish_book_list = user.guest.own_book_set.all().filter(status=Book.STATUS['finish'])
#		for book in book_list:
#			if Book.STATUS == Book.STATUS['finish']:
#				finish_book_list.append(book)
#			else:
#				edit_book_list.append(book)
		return locals()

	@method_decorator(user_category_check(['guest']))
	@method_decorator(http_response)
	def post(self, request, *args, **kwargs):
		readme_url = request.path +'readme/'
		template_name=self.template_name
		user=request.user
		if request.POST.has_key('emailBook'):
			book_ISBN = request.POST.get('emailBook')
			emailBook = Book.objects.get(ISBN = book_ISBN)
			subject = u'[文件] {}'.format(emailBook.book_info.bookname)
			body = u'新愛的{0}您好：\n'.format(user.username)
			email = EmailMessage(subject=subject, body=body, from_email=SERVICE, to=[user.email])
			attach_file_path = emailBook.zip(user, 'test')
			if attach_file_path == '':
				status = 'error'
				message = u'附加文件失敗'
				return locals()
			email.attach_file(attach_file_path)
#			for part in emailBook.ebook_set.all():
#				attach_file_path = emailBook.path +u'/OCR/part{0}.txt'.format(part.part)
#				email.attach_file(attach_file_path)
			email.send(fail_silently=False)
			status = 'success'
			message = u'已寄送到您的電子信箱'
		if request.POST.has_key('delete'):
			book_ISBN = request.POST.get('delete')
			deleteBook = Book.objects.get(ISBN = book_ISBN)
			deletePath = deleteBook.path
			shutil.rmtree(deletePath)
			deleteBook.delete()
			status = 'success'
			message = u'成功刪除文件'
		book_list = user.guest.own_book_set.all()
		edit_book_list = user.guest.own_book_set.all().exclude(status=Book.STATUS['edit'])
		finish_book_list = user.guest.own_book_set.all().filter(status=Book.STATUS['finish'])
		return locals()
