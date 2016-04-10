# coding: utf-8
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
from utils.vaildate import *
from utils.zip import *
import mysite

MANAGER = ['tsengwoody@yahoo.com.tw']
SERVICE = 'tsengwoody.tw@gmail.com'

@user_category_check('guest')
def create_document(request, template_name='guest/create_document.html'):
	if request.method == 'POST':
		bookForm = BookForm(request.POST, request.FILES)
		if bookForm.is_valid():
			uploadPath = u'static/ebookSystem/document/{0}'.format(bookForm.cleaned_data['ISBN'])
			if not os.path.exists(uploadPath):
				uploadFilePath = handle_uploaded_file(uploadPath, request.FILES['fileObject'])
				with ZipFile(uploadFilePath, 'r') as uploadFile:
					ZipFile.testzip(uploadFile)
				unzip_file(uploadFilePath, uploadPath)
				if vaildate_folder(uploadPath+u'/OCR', uploadPath+u'/source', 50)[0]:
					bookForm.save()
			else:
				errors_message = u'文件已存在'
	if request.method == 'GET':
		bookForm = BookForm()
	return render(request, template_name, locals())

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
		from django.utils import simplejson
		cache_key = "%s_%s" % (request.META['REMOTE_ADDR'], progress_id)
		data = cache.get(cache_key)
		return HttpResponse(simplejson.dumps(data))
	else:
		return HttpResponseServerError('Server Error: You must provide X-Progress-ID header or query param.')

def upload(request, template_name='guest/upload.html'):
	if request.method == 'POST':
#		if request.is_ajax():
		data = 'ajax_test'
		return HttpResponse(simplejson.dumps(data), content_type="application/ajax")
#	if request.method == 'GET':
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
				attach_file_path = emailBook.path +u'/OCR/part{0}.txt'.format(part.part)
				email.attach_file(attach_file_path)
			email.send(fail_silently=False)
		return render(request, template_name, locals())