# coding: utf-8
from django.contrib import messages
from django.core.cache import cache
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseServerError 
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import generic
from zipfile import ZipFile
from ebookSystem.models import *
from account.models import *
from .models import *
from .forms import *
from utils.decorator import *
from utils.validate import *
from utils.uploadFile import handle_uploaded_file
from utils.zip import *
from mysite.settings import PREFIX_PATH,INACTIVE, ACTIVE, EDIT, REVIEW, REVISE, FINISH
import zipfile
import json
import shutil

@user_category_check(['scaner'])
@http_response
def create_document(request, template_name='guest/create_document.html'):
	readme_url = request.path +'readme/'
	user = request.user
	if request.method == 'POST':
		bookForm = BookForm(request.POST, request.FILES)
		if not bookForm.is_valid():
			status = 'error'
			message = u'表單驗證失敗' +str(bookForm.errors)
			return locals()
		uploadPath = PREFIX_PATH +u'static/ebookSystem/document/{0}'.format(bookForm.cleaned_data['ISBN'])
		if os.path.exists(uploadPath):
			status = 'error'
			message = u'文件已存在'
			return locals()
		[status, message] = handle_uploaded_file(uploadPath, request.FILES['fileObject'])
		uploadFilePath = os.path.join(uploadPath, request.FILES['fileObject'].name)
		try:
			with ZipFile(uploadFilePath, 'r') as uploadFile:
				ZipFile.testzip(uploadFile)
		except:
				shutil.rmtree(uploadPath)
				status = 'error'
				message = u'非正確ZIP文件'
				return locals()
		unzip_file(uploadFilePath, uploadPath)
		newBook = bookForm.save(commit=False)
		newBook.path = uploadPath
		if not newBook.validate_folder():
			shutil.rmtree(uploadPath)
			status = 'error'
			message = u'上傳壓縮文件結構錯誤，詳細結構請參考說明頁面'
			return locals()
		newBook.scaner = user
		newBook.save()
		newBook.create_EBook()
		if request.POST.has_key('guest'):
			try:
				guest = Guest.objects.get(user__username=request.POST['guest'])
				newBook.guests.add(guest)
			except:
				guest = None
		else:
			guest = None
		redirect_to = reverse('guest:profile')
		status = 'success'
		message = u'成功建立並上傳文件'
		return locals()
	if request.method == 'GET':
		bookForm = BookForm()
		return locals()

def upload_progress(request):
	"""
	Return JSON object with information about the progress of an upload.
	"""
	progress_id = ''
	if 'X-Progress-ID' in request.GET:
		progress_id = request.GET['X-Progress-ID']
	elif 'X-Progress-ID' in request.META:
		progress_id = request.META['X-Progress-ID']
	if progress_id:
		cache_key = "%s_%s" % (request.META['REMOTE_ADDR'], progress_id)
		data = cache.get(cache_key)
#		cache_key = "%s" % (progress_id)
#		data = request.session.get('upload_progress_%s' % cache_key, None)
		return HttpResponse(json.dumps(data), content_type="application/json")
	else:
		return HttpResponseServerError('Server Error: You must provide X-Progress-ID header or query param.')

class profileView(generic.View):
	template_name=''

	@method_decorator(user_category_check(['guest']))
	@method_decorator(http_response)
	def get(self, request, *args, **kwargs):
		readme_url = request.path +'readme/'
		template_name=self.template_name
		user=request.user
		book_list = user.guest.own_book_set.all()
		edit_book_list = []
		finish_book_list = []
		for book in book_list:
			if book.status == FINISH:
				finish_book_list.append(book)
			else:
				edit_book_list.append(book)
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
			for part in emailBook.ebook_set.all():
				attach_file_path = emailBook.path +u'/OCR/part{0}.txt'.format(part.part)
				email.attach_file(attach_file_path)
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
		edit_book_list = []
		finish_book_list = []
		for book in book_list:
			if book.status == FINISH:
				finish_book_list.append(book)
			else:
				edit_book_list.append(book)
		return locals()
