# coding: utf-8
import codecs
import datetime
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone
from django.views import generic
from .models import *
from .forms import *
import os
import mysite
import json

class book_list(generic.ListView):
	model = Book
	def get_queryset(self):
		return Book.objects.order_by('-bookname')

def detail(request, book_ISBN, template_name='ebookSystem/detail.html'):
	try:
		book = Book.objects.get(ISBN=book_ISBN)
	except Book.DoesNotExist:
		raise Http404("book does not exist")
	return render(request, template_name, locals())

def edit_ajax(request, book_ISBN, part_part, *args, **kwargs):
	user = request.user
	book = Book.objects.get(ISBN=book_ISBN)
	part = EBook.objects.get(part=part_part,book=book)
	if 'online' in request.POST:
		user.online = timezone.now()
		user.save()
		part.service_hours = part.service_hours+1
		part.save()
		response['status'] = 'success'
		response['message'] = part.service_hours
#	elif 'user_status' in request.POST and request.POST['user_status'] == 'edit':
#		editor.is_editing = True
#		response['status'] = 'success'
#	elif 'user_status' in request.POST and request.POST['user_status'] == 'profile':
#		editor.is_editing = False
#		response['status'] = 'success'
	else:
		response['status'] = 'error'
	return HttpResponse(json.dumps(response), content_type="application/json")

class editView(generic.View):
	def get(self, request, encoding='utf-8', *args, **kwargs):
		template_name='ebookSystem/edit.html'
		try:
			book = Book.objects.get(ISBN=kwargs['book_ISBN'])
			part = EBook.objects.get(part=kwargs['part_part'],book=book)
		except book.DoesNotExist:
			raise Http404("book or part does not exist")
		finishContent=''
		editContent=''
		fileHead=''
		[scanPageList, defaultPageIndex, defaultPage, defaultPageURL] = editVarInit(book, part)
		finishFilePath = book.path+u'/OCR/part{0}-finish.txt'.format(part.part)
#		finishFilePath = finishFilePath.encode('utf-8')
		filePath = book.path+u'/OCR/part{1}.txt'.format(book.bookname, part.part)
#		filePath = filePath.encode('utf-8')
		[finishContent, editContent, fileHead] = getContent(filePath)
		with codecs.open(finishFilePath, 'w', encoding=encoding) as fileWrite:
			if finishContent!='':
				fileWrite.write(fileHead+finishContent)
			else:
				fileWrite.write(fileHead)
		editForm = EditForm({'content':editContent,'page':defaultPageIndex})
		return render(request, template_name, locals())
	def post(self, request, encoding='utf-8', *args, **kwargs):
		template_name='ebookSystem/edit.html'
		try:
			book = Book.objects.get(ISBN=kwargs['book_ISBN'])
			part = EBook.objects.get(part=kwargs['part_part'],book=book)
		except book.DoesNotExist:
			raise Http404("book or part does not exist")
		[scanPageList, defaultPageIndex, defaultPage, defaultPageURL] = editVarInit(book, part)
		editForm = EditForm(request.POST)
		finishFilePath = book.path+u'/OCR/part{0}-finish.txt'.format(part.part)
#		finishFilePath = finishFilePath.encode('utf-8')
		filePath = book.path+u'/OCR/part{1}.txt'.format(book.bookname, part.part)
#		filePath = filePath.encode('utf-8')
		if request.POST.has_key('save'):
			if editForm.is_valid():
				editContent=editForm.cleaned_data['content']
				with codecs.open(finishFilePath, 'r', encoding=encoding) as fileRead:
					finishContent=fileRead.read()
				with codecs.open(filePath, 'w', encoding=encoding) as fileWrite:
					fileWrite.write(finishContent+editContent)
				part.edited_page=editForm.cleaned_data['page']
				part.edit_date = timezone.now()
				part.save()
				[finishContent, editContent, fileHead] = getContent(filePath)
				[scanPageList, defaultPageIndex, defaultPage, defaultPageURL] = editVarInit(book, part)
				with codecs.open(finishFilePath, 'w', encoding=encoding) as fileWrite:
					if finishContent!='':
						fileWrite.write(fileHead+finishContent)
					else:
						fileWrite.write(fileHead)
				editForm = EditForm({'content':editContent,'page':part.edited_page})
				message=u'您上次儲存時間為：{0}，請定時存檔喔~'.format(part.edit_date)
				return render(request, template_name, locals())
			else:
				message=u'表單驗證失敗'
				return render(request, template_name, locals())
		elif request.POST.has_key('close'):
			return HttpResponseRedirect(reverse('account:profile'))
		elif request.POST.has_key('finish'):
			if editForm.is_valid() and editForm.cleaned_data['content'].find('|----------|') == -1:
				editContent=editForm.cleaned_data['content']
				with codecs.open(finishFilePath, 'r', encoding=encoding) as fileRead:
					finishContent=fileRead.read()
				with codecs.open(filePath, 'w', encoding=encoding) as fileWrite:
					fileWrite.write(finishContent+editContent)
				part.edited_page=editForm.cleaned_data['page']
				part.is_finish = True
				part.finish_date = timezone.now()
				part.edit_date = timezone.now()
				part.save()
				return HttpResponseRedirect(reverse('account:profile'))
			else:
				message=u'表單驗證失敗'
				return render(request, template_name, locals())

def editVarInit(book, part):
	sourcePath = book.path +u'/source'
#	sourcePath = sourcePath.encode('utf-8')
	fileList=os.listdir(sourcePath)
	scanPageList=[]
	for scanPage in fileList:
		if scanPage.split('.')[-1]=='jpg':
			scanPageList.append(scanPage)
	scanPageList = scanPageList[part.begin_page:part.end_page+1]
	defaultPageIndex=part.edited_page
	defaultPage=scanPageList[defaultPageIndex]
	defaultPageURL = sourcePath +u'/' +defaultPage
	defaultPageURL=defaultPageURL.replace(mysite.settings.PREFIX_PATH +'static/', '')
	return [scanPageList, defaultPageIndex, defaultPage, defaultPageURL]

def getContent(contentPath, encoding='utf-8'):
	finishContent=''
	editContent=''
	with codecs.open(contentPath, 'r', encoding=encoding) as fileRead:
		firstLine=fileRead.next()
		fileHead=firstLine[0]
		finishContent=firstLine[1:]
		finishFlag=False
		if finishContent=='|----------|\r\n':
			finishContent=''
			finishFlag=True
		finishCount=1
		if not finishFlag:
			for i in fileRead:
				finishCount=finishCount+1
				if i=='|----------|\r\n':
					finishFlag=True
					break
				finishContent = finishContent+i
		editCount=0
		for i in fileRead:
			editCount = editCount+1
			editContent = editContent+i
		if editContent == '':
			editContent = finishContent
			finishContent = ''
	return [finishContent, editContent, fileHead]