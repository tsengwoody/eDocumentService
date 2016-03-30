# coding: utf-8
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import generic
from ebookSystem.models import *
from account.models import *
from .models import *
from .forms import *
from utils.decorator import *
from utils.vaildate import *
from utils.zip import *
import mysite

MANAGER = ['tsengwoody@yahoo.com.tw']
SERVICE = 'tsengwoody.tw@gmail.com'

def book_save_test(request, template_name='guest/book_save_test.html'):
	if request.method == 'POST':
		bookForm = BookFormTest(request.POST)
		if bookForm.is_valid():
			bookForm.save()
	if request.method == 'GET':
		bookForm = BookFormTest()
	return render(request, template_name, locals())

@user_category_check('guest')
def create_document(request, template_name='guest/create_document.html'):
	if request.method == 'POST':
		bookForm = BookForm(request.POST, request.FILES)
		if bookForm.is_valid():
			uploadPath = u'static/ebookSystem/document/{0}'.format(bookForm.cleaned_data['bookname'])
			if not os.path.exists(uploadPath):
				uploadFilePath = handle_uploaded_file(uploadPath, request.FILES['fileObject'])
				unzip_file(uploadFilePath, uploadPath)
				if vaildate_folder(uploadPath+u'/OCR', uploadPath+u'/source', 50)[0]:
					bookForm.save()
			else:
				errors_message = u'文件已存在'
	if request.method == 'GET':
		bookForm = BookForm()
	return render(request, template_name, locals())


def upload(request, template_name='guest/upload.html'):
	if request.method == 'POST':
		print type(request.FILES)
		bookForm = BookForm(request.POST, request.FILES)
		if bookForm.is_valid():
			uploadPath = u'static/ebookSystem/document/{0}'.format(bookForm.cleaned_data['bookname'])
			uploadFilePath = handle_uploaded_file(uploadPath, request.FILES['fileObject'])
			unzip_file(uploadFilePath, uploadPath)
			bookForm = BookForm(request.POST, request.FILES)
	if request.method == 'GET':
		bookForm = BookForm(request.POST, request.FILES)
	return render(request, template_name, locals())

def handle_uploaded_file(dirname, file):
	if not os.path.exists(dirname):
		os.makedirs(dirname, 0777)
	fullpath = dirname +u'/' +file.name
	if os.path.exists(fullpath):
		return -1
	with open(fullpath, 'wb+') as destination:
		for chunk in file.chunks():
			destination.write(chunk)
	return fullpath

class profileView(generic.View):
	template_name=''

	@method_decorator(user_category_check('guest'))
	def get(self, request, *args, **kwargs):
		template_name=self.template_name
		user=request.user
		book_list = Book.objects.filter(guest=user.guest)
		return render(request, template_name, locals())

	@method_decorator(user_category_check('guest'))
	def post(self, request, *args, **kwargs):
		template_name=self.template_name
		user=request.user
		book_list = Book.objects.filter(guest=user.guest)
		if request.POST.has_key('emailBook'):
			book_ISBN = request.POST.get('emailBook')
			emailBook = Book.objects.get(ISBN = book_ISBN)
			subject = u'[文件] {}'.format(emailBook.bookname)
			body = u'新愛的{0}您好：\n'.format(user.username)
			email = EmailMessage(subject=subject, body=body, from_email=SERVICE, to=[user.email])
			for part in emailBook.ebook_set.all():
				attach_file_path = mysite.settings.PREFIX_PATH +emailBook.path +u'/OCR/part{0}.txt'.format(part.part)
				email.attach_file(attach_file_path)
			email.send(fail_silently=False)
			print 'send email'
		return render(request, template_name, locals())