# coding: utf-8
import codecs
import datetime
from django.shortcuts import render
from django.http import HttpResponseRedirect

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
	editUrl=[]
	for i in range(book.partCount):
		editUrl.append('/ebookSystem/edit/'+str(book.id)+'/'+str(i+1))
	return render(request, template_name, locals())

def editbook(request, book_id, template_name='ebookSystem/edit.html'):
	finishContent=''
	editContent=''
	fileHead=''
	try:
		book = Book.objects.get(pk=book_id)
	except book.DoesNotExist:
		raise Http404("book does not exist")
	if request.method == 'POST':
		editForm = EditForm(request.POST)
		if editForm.is_valid():
			editContent=editForm.cleaned_data['content']
			with codecs.open('{0}_finish.txt'.format(book.id), 'r', encoding='utf-16le') as fileRead:
				finishContent=fileRead.read()
			with codecs.open('{0}.txt'.format(book.id), 'w', encoding='utf-16le') as fileWrite:
				fileWrite.write(finishContent+editContent)
			[finishContent, editContent, fileHead] = getContent('{0}.txt'.format(book.id))
			with codecs.open('{0}_finish.txt'.format(book.id), 'w', encoding='utf-16le') as fileWrite:
				fileWrite.write(fileHead+finishContent)
			editForm = EditForm({'content':editContent,'page':1})
			editTime=datetime.datetime.now()
			return render(request, template_name, locals())
#		else:
	if request.method == 'GET':
		[finishContent, editContent, fileHead] = getContent('{0}.txt'.format(book.id))
		with codecs.open('{0}_finish.txt'.format(book.id), 'w', encoding='utf-16le') as fileWrite:
			fileWrite.write(fileHead+finishContent)
		editForm = EditForm({'content':editContent,'page':1})
		return render(request, template_name, locals())

def getContent(contentPath, encoding='utf-16le'):
	finishContent=''
	editContent=''
	with codecs.open(contentPath, 'r', encoding=encoding) as fileRead:
		firstLine=fileRead.next()
		fileHead=firstLine[0]
		finishContent=firstLine[1:]
		finishCount=1
		for i in fileRead:
			finishCount=finishCount+1
			if i=='|----------|\r\n':
				break
			finishContent=finishContent+i
		editCount=0
		for i in fileRead:
			editCount=editCount+1
			editContent=editContent+i
	return [finishContent, editContent, fileHead]

class editView(generic.View):
	def get(self, request, *args, **kwargs):
		template_name='ebookSystem/edit.html'
		finishContent=''
		editContent=''
		fileHead=''
		[book, part, scanPageList, defaultPageIndex, defaultPage, defaultPageURL] = editVarInit(kwargs['book_id'], kwargs['part_id'])
		finishFilePath=book.path+u'/{0}-finish.txt'.format(book.bookname)
		filePath=book.path+u'/{0}.txt'.format(book.bookname)
		[finishContent, editContent, fileHead] = getContent(filePath)
		with codecs.open(finishFilePath, 'w', encoding='utf-16le') as fileWrite:
			fileWrite.write(fileHead+finishContent)
		editForm = EditForm({'content':editContent,'page':defaultPageIndex})
		return render(request, template_name, locals())
	def post(self, request, *args, **kwargs):
		template_name='ebookSystem/edit.html'
		[book, part, scanPageList, defaultPageIndex, defaultPage, defaultPageURL] = editVarInit(kwargs['book_id'], kwargs['part_id'])
		editForm = EditForm(request.POST)
		finishFilePath=book.path+u'/{0}-finish.txt'.format(book.bookname)
		filePath=book.path+u'/{0}.txt'.format(book.bookname)
		if editForm.is_valid() and editForm.cleaned_data['content'].find('|----------|') != -1:
			editContent=editForm.cleaned_data['content']
			with codecs.open(finishFilePath, 'r', encoding='utf-16le') as fileRead:
				finishContent=fileRead.read()
			with codecs.open(filePath, 'w', encoding='utf-16le') as fileWrite:
				fileWrite.write(finishContent+editContent)
			part.editedPage=editForm.cleaned_data['page']
			part.save()
			[finishContent, editContent, fileHead] = getContent(filePath)
			[book, part, scanPageList, defaultPageIndex, defaultPage, defaultPageURL] = editVarInit(kwargs['book_id'], kwargs['part_id'])
			with codecs.open(finishFilePath, 'w', encoding='utf-16le') as fileWrite:
				fileWrite.write(fileHead+finishContent)
			editForm = EditForm({'content':editContent,'page':part.editedPage})
			editTime=datetime.datetime.now()
			message=u'您上次儲存時間為：{0}，請定時存檔喔~'.format(editTime)
			return render(request, template_name, locals())
		else:
			message=u'未儲存成功，您提交的內容未包含特殊標記，無法得知校對進度'
			return render(request, template_name, locals())

def editVarInit(book_id,part_id):
	try:
		book = Book.objects.get(pk=book_id)
		part = EBook.objects.get(part=part_id,book=book)
	except book.DoesNotExist:
		raise Http404("book or part does not exist")
	fileList=os.listdir(book.path+u'/source')
	scanPageList=[]
	for scanPage in fileList:
		if scanPage.split('.')[-1]=='jpg':
			scanPageList.append(scanPage)
	scanPageList = scanPageList[part.beginPage:part.endPage+1]
	defaultPageIndex=part.editedPage
	defaultPage=scanPageList[defaultPageIndex]
	defaultPageURL = book.path+u'/source/'+defaultPage
	defaultPageURL=defaultPageURL.lstrip('static/')
	return [book, part, scanPageList, defaultPageIndex, defaultPage, defaultPageURL]