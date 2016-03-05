# coding: utf-8
import codecs
import datetime
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

# Create your views here.
from django.views import generic
from .models import *
from .forms import *
import os

class book_list(generic.ListView):
	model = Book
	def get_queryset(self):
		return Book.objects.order_by('-bookname')

def detail(request, book_id, template_name='ebookSystem/detail.html'):
	try:
		book = Book.objects.get(pk=book_id)
	except book.DoesNotExist:
		raise Http404("book does not exist")
	partList = book.ebook_set.all()
	return render(request, template_name, locals())

def viewSource(request, book_id, page, template_name='ebookSystem/viewSource.html'):
	try:
		book = Book.objects.get(pk=book_id)
	except book.DoesNotExist:
		raise Http404("book does not exist")
	pageURL = book.path+u'/source/'+page
	pageURL=pageURL.lstrip('static/')
	return render(request, template_name, locals())

class editView(generic.View):
	def get(self, request, *args, **kwargs):
		template_name='ebookSystem/edit.html'
		try:
			book = Book.objects.get(pk=kwargs['book_id'])
			part = EBook.objects.get(part=kwargs['part_id'],book=book)
		except book.DoesNotExist:
			raise Http404("book or part does not exist")
		finishContent=''
		editContent=''
		fileHead=''
		[scanPageList, defaultPageIndex, defaultPage, defaultPageURL] = editVarInit(book, part)
		finishFilePath=book.path+u'/OCR/part{0}-finish.txt'.format(part.part)
		filePath=book.path+u'/OCR/part{1}.txt'.format(book.bookname, part.part)
		[finishContent, editContent, fileHead] = getContent(filePath)
		with codecs.open(finishFilePath, 'w', encoding='utf-16le') as fileWrite:
			if finishContent!=[]:
				fileWrite.write(fileHead+finishContent)
			else:
				fileWrite.write(fileHead)
		editForm = EditForm({'content':editContent,'page':defaultPageIndex})
		return render(request, template_name, locals())
	def post(self, request, *args, **kwargs):
		template_name='ebookSystem/edit.html'
		try:
			book = Book.objects.get(pk=kwargs['book_id'])
			part = EBook.objects.get(part=kwargs['part_id'],book=book)
		except book.DoesNotExist:
			raise Http404("book or part does not exist")
		[scanPageList, defaultPageIndex, defaultPage, defaultPageURL] = editVarInit(book, part)
		editForm = EditForm(request.POST)
		finishFilePath=book.path+u'/OCR/part{0}-finish.txt'.format(part.part)
		filePath=book.path+u'/OCR/part{1}.txt'.format(book.bookname, part.part)
		if request.POST.has_key('save'):
			if editForm.is_valid():
				editContent=editForm.cleaned_data['content']
				with codecs.open(finishFilePath, 'r', encoding='utf-16le') as fileRead:
					finishContent=fileRead.read()
				with codecs.open(filePath, 'w', encoding='utf-16le') as fileWrite:
					fileWrite.write(finishContent+editContent)
				part.edited_page=editForm.cleaned_data['page']
				part.edit_date = datetime.date.today()
				part.save()
				[finishContent, editContent, fileHead] = getContent(filePath)
				[scanPageList, defaultPageIndex, defaultPage, defaultPageURL] = editVarInit(book, part)
				with codecs.open(finishFilePath, 'w', encoding='utf-16le') as fileWrite:
					if finishContent!=[]:
						fileWrite.write(fileHead+finishContent)
					else:
						fileWrite.write(fileHead)
				editTime=datetime.datetime.now()
				editForm = EditForm({'content':editContent,'page':part.edited_page})
				message=u'您上次儲存時間為：{0}，請定時存檔喔~'.format(editTime)
				return render(request, template_name, locals())
			else:
				message=u'表單驗證失敗'
				return render(request, template_name, locals())
		elif request.POST.has_key('close'):
			return HttpResponseRedirect(reverse('account:profile'))
		elif request.POST.has_key('finish'):
			if editForm.is_valid() and editForm.cleaned_data['content'].find('|----------|') == -1:
				editContent=editForm.cleaned_data['content']
				with codecs.open(finishFilePath, 'r', encoding='utf-16le') as fileRead:
					finishContent=fileRead.read()
				with codecs.open(filePath, 'w', encoding='utf-16le') as fileWrite:
					fileWrite.write(finishContent+editContent)
				part.edited_page=editForm.cleaned_data['page']
				part.is_finish = True
				part.is_edited = False
				part.edit_date = datetime.date.today()
				part.save()
				return HttpResponseRedirect(reverse('account:profile'))
			else:
				message=u'表單驗證失敗'
				return render(request, template_name, locals())

def editVarInit(book, part):
	fileList=os.listdir(book.path+u'/source')
	scanPageList=[]
	for scanPage in fileList:
		if scanPage.split('.')[-1]=='jpg':
			scanPageList.append(scanPage)
	scanPageList = scanPageList[part.begin_page:part.end_page+1]
	defaultPageIndex=part.edited_page
	defaultPage=scanPageList[defaultPageIndex]
	defaultPageURL = book.path+u'/source/'+defaultPage
	defaultPageURL=defaultPageURL.lstrip('static/')
	return [scanPageList, defaultPageIndex, defaultPage, defaultPageURL]

def getContent(contentPath, encoding='utf-16le'):
	finishContent=''
	editContent=''
	with codecs.open(contentPath, 'r', encoding=encoding) as fileRead:
		firstLine=fileRead.next()
		fileHead=firstLine[0]
		finishContent=firstLine[1:]
		finishFlag=False
		if finishContent=='|----------|\r\n':
			finishContent=[]
			finishFlag=True
		finishCount=1
		if finishContent!=[]:
			for i in fileRead:
				finishCount=finishCount+1
				if i=='|----------|\r\n':
					finishFlag=True
					break
				finishContent=finishContent+i
		editCount=0
		for i in fileRead:
			editCount=editCount+1
			editContent=editContent+i
	return [finishContent, editContent, fileHead]