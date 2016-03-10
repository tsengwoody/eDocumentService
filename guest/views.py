# coding: utf-8
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse
from ebookSystem.models import *
from ebookSystem.forms import *
from .forms import *
from .zip import *

def create_document(request, template_name='guest/create_document.html'):
	if request.method == 'POST':
		bookForm = BookForm(request.POST)
		if bookForm.is_valid():
			uploadPath = u'static/ebookSystem/document/{0}'.format(bookForm.cleaned_data['bookname'])
			uploadFilePath = handle_uploaded_file(uploadPath, request.FILES['fileObject'])
			unzip_file(uploadFilePath, newBook.path)
			newBook = bookForm.save()
	if request.method == 'GET':
		bookForm = BookForm()
	return render(request, template_name, locals())

def upload(request, template_name='guest/upload.html'):
	if request.method == 'POST':
#		uploadForm = UploadForm(request.POST, request.FILES)
#		if uploadForm.is_valid():
		uploadFilePath = handle_uploaded_file(request.POST['path'], request.FILES['fileObject'])
		unzip_file(uploadFilePath, newBook.path)
		uploadForm = UploadForm()
	if request.method == 'GET':
		uploadForm = UploadForm()
	return render(request, template_name, locals())

def handle_uploaded_file(dirname, file):
	if not os.path.exists(dirname):
		os.mkdir(dirname, 0777)
	fullpath = dirname +u'/' +file.name
	if os.path.exists(fullpath):
		return -1
	with open(fullpath, 'wb+') as destination:
		for chunk in file.chunks():
			destination.write(chunk)
	return fullpath