# coding: utf-8
import codecs
import datetime
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect,HttpResponse, Http404
from django.shortcuts import render
from django.utils import timezone
from django.views import generic
from .models import *
from .forms import *
from mysite.settings import PREFIX_PATH,INACTIVE, ACTIVE, EDIT, REVIEW, REVISE, FINISH
import os
import json
import shutil

class book_list(generic.ListView):
	model = Book
	def get_queryset(self):
		return Book.objects.order_by('-bookname')

def search_book(request, template_name='ebookSystem/search_book.html'):
	if request.method == 'GET':
		return render(request, template_name, locals())
	if request.method == 'POST':
		response = {}
		redirect_to = None
		if request.POST.has_key('book_ISBN'):
			book_ISBN = request.POST['book_ISBN']
			book_list = Book.objects.filter(ISBN=book_ISBN)
			if len(book_list) > 0:
				response['status'] = 'success'
				response['message'] = u'成功查詢資料'
			else:
				response['status'] = 'error'
				response['message'] = u'查無資料'
		elif request.POST.has_key('get_book'):
			book_ISBN = request.POST['get_book']
			book = Book.objects.get(ISBN=book_ISBN)
			guest = Guest.objects.get(user=request.user)
			book.guests.add(guest)
			response['status'] = 'success'
			response['message'] = u'獲取成功請到個人頁面進行email傳送'
		status = response['status']
		message = response['message']
		if request.is_ajax():
			return HttpResponse(json.dumps(response), content_type="application/json")
		else:
#			if redirect_to:
#				return HttpResponseRedirect(redirect_to)
#			else:
			return render(request, template_name, locals())



def review_document(request, book_ISBN, template_name='ebookSystem/review_document.html'):
	try:
		book = Book.objects.get(ISBN=book_ISBN)
	except:
		raise Http404("book does not exist")
	sourcePath = book.path +u'/source'
#		sourcePath = sourcePath.encode('utf-8')
	fileList=os.listdir(sourcePath)
	scanPageList=[]
	for scanPage in fileList:
		if scanPage.split('.')[-1].lower() == 'jpg':
			scanPageList.append(scanPage)
	defaultPage=scanPageList[0]
	defaultPageURL = sourcePath +u'/' +defaultPage
	defaultPageURL=defaultPageURL.replace(PREFIX_PATH +'static/', '')
	if request.method == 'GET':
		return render(request, template_name, locals())
	if request.method == 'POST':
		response = {}
		redirect_to = None
		if request.POST['review'] == 'success':
			book.is_active = True
			book.save()
			response['status'] = 'success'
			response['message'] = u'審核通過文件'
			response['redirect_to'] = reverse('manager:review_document_list')
		if request.POST['review'] == 'error':
			shutil.rmtree(book.path)
			book.delete()
			response['status'] = 'success'
			response['message'] = u'審核退回文件'
			response['redirect_to'] = reverse('manager:review_document_list')
		status = response['status']
		message = response['message']
		redirect_to = response['redirect_to']
		if request.is_ajax():
			return HttpResponse(json.dumps(response), content_type="application/json")
		else:
			if redirect_to:
				return HttpResponseRedirect(redirect_to)
			else:
				return render(request, template_name, locals())

def review_part(request, ISBN_part, template_name='ebookSystem/review_part.html'):
	try:
		part = EBook.objects.get(ISBN_part=ISBN_part)
	except:
		raise Http404("book does not exist")
	finishFilePath = part.book.path +'/OCR/part{}.txt'.format(part.part)
	content =''
	with codecs.open(finishFilePath, 'r', encoding='utf-8') as fileRead:
		content = fileRead.read()
	if request.method == 'GET':
		return render(request, template_name, locals())
	if request.method == 'POST':
		response = {}
		redirect_to = None
		if request.POST['review'] == 'success':
			part.status = FINISH
			part.save()
			response['status'] = 'success'
			response['message'] = u'審核通過文件'
			response['redirect_to'] = reverse('manager:review_part_list')
		if request.POST['review'] == 'error':
			part.status = REVISE
			part.save()
			response['status'] = 'success'
			response['message'] = u'審核退回文件'
			response['redirect_to'] = reverse('manager:review_part_list')
		status = response['status']
		message = response['message']
		redirect_to = response['redirect_to']
		if request.is_ajax():
			return HttpResponse(json.dumps(response), content_type="application/json")
		else:
			if redirect_to:
				return HttpResponseRedirect(redirect_to)
			else:
				return render(request, template_name, locals())

def detail(request, book_ISBN, template_name='ebookSystem/detail.html'):
	try:
		book = Book.objects.get(ISBN=book_ISBN)
	except:
		raise Http404("book does not exist")
	return render(request, template_name, locals())

def edit_ajax(request, book_ISBN, part_part, *args, **kwargs):
	user = request.user
	response={}
	book = Book.objects.get(ISBN=book_ISBN)
	part = EBook.objects.get(part=part_part,book=book)
	response = {}
	if 'online' in request.POST:
		if not user.online:
			user.online = timezone.now()
			user.save()
		delta = timezone.now() - user.online
		if delta.seconds < 50:
			response['status'] = 'error'
			response['message'] = u'您有其他編輯正進行'
		else:
			user.online = timezone.now()
			user.save()
			part.service_hours = part.service_hours+1
			part.save()
			response['status'] = 'success'
			response['message'] = part.service_hours
	else:
		response['status'] = 'error'
	return HttpResponse(json.dumps(response), content_type="application/json")

class editView(generic.View):
	def get(self, request, encoding='utf-8', *args, **kwargs):
		template_name='ebookSystem/edit.html'
		user = request.user
		response = {}
		try:
			book = Book.objects.get(ISBN=kwargs['book_ISBN'])
			part = EBook.objects.get(part=kwargs['part_part'],book=book)
		except: 
			raise Http404("book or part does not exist")
		finishContent=''
		editContent=''
		fileHead=''
		[scanPageList, defaultPageIndex, defaultPage, defaultPageURL] = editVarInit(part)
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
		return render(request, template_name, locals())

	def post(self, request, encoding='utf-8', *args, **kwargs):
		template_name='ebookSystem/edit.html'
		response = {}
		try:
			book = Book.objects.get(ISBN=kwargs['book_ISBN'])
			part = EBook.objects.get(part=kwargs['part_part'],book=book)
		except:
			raise Http404("book or part does not exist")
		[scanPageList, defaultPageIndex, defaultPage, defaultPageURL] = editVarInit(part)
		editForm = EditForm(request.POST)
		finishFilePath = book.path+u'/OCR/part{0}-finish.txt'.format(part.part)
#		finishFilePath = finishFilePath.encode('utf-8')
		filePath = book.path+u'/OCR/part{1}.txt'.format(book.bookname, part.part)
#		filePath = filePath.encode('utf-8')
		if request.POST.has_key('save'):
			editContent = request.POST['content']
			with codecs.open(finishFilePath, 'r', encoding=encoding) as fileRead:
				finishContent=fileRead.read()
			with codecs.open(filePath, 'w', encoding=encoding) as fileWrite:
				fileWrite.write(finishContent+editContent)
			part.edited_page=int(request.POST['page'])
			part.save()
			[finishContent, editContent, fileHead] = getContent(filePath)
			[scanPageList, defaultPageIndex, defaultPage, defaultPageURL] = editVarInit(part)
			with codecs.open(finishFilePath, 'w', encoding=encoding) as fileWrite:
				if finishContent!='':
					fileWrite.write(fileHead+finishContent)
				else:
					fileWrite.write(fileHead)
			response['status'] = 'success'
			response['message'] = u'您上次儲存時間為：{0}，請定時存檔喔~'.format(timezone.now())
		elif request.POST.has_key('close'):
			response['status'] = ['success',u'error']
			response['message'] = [u'close', u'error message']
			response['redirect_to'] = reverse('account:profile')
			redirect_to = response['redirect_to']
		elif request.POST.has_key('finish'):
			editContent = request.POST['content']
			with codecs.open(finishFilePath, 'r', encoding=encoding) as fileRead:
				finishContent=fileRead.read()
			with codecs.open(filePath, 'w', encoding=encoding) as fileWrite:
				fileWrite.write(finishContent+editContent)
			part.edited_page = int(request.POST['page'])
			part.status = REVIEW
			part.finish_date = timezone.now()
			part.save()
			[finishContent, editContent, fileHead] = getContent(filePath)
			[scanPageList, defaultPageIndex, defaultPage, defaultPageURL] = editVarInit(part)
			with codecs.open(finishFilePath, 'w', encoding=encoding) as fileWrite:
				if finishContent!='':
					fileWrite.write(fileHead+finishContent)
				else:
					fileWrite.write(fileHead)
			response['status'] = 'success'
			response['message'] = u'您上次儲存時間為：{0}，請定時存檔喔~'.format(timezone.now())
			response['redirect_to'] = reverse('account:profile')
		status = response['status']
		message = response['message']
		if request.is_ajax():
			return HttpResponse(json.dumps(response), content_type="application/json")
		else:
			return render(request, template_name, locals())

def editVarInit(part):
	sourcePath = part.book.path +u'/source'
#	sourcePath = sourcePath.encode('utf-8')
	fileList=os.listdir(sourcePath)
	scanPageList=[]
	for scanPage in fileList:
		if scanPage.split('.')[-1].lower() == 'jpg':
			scanPageList.append(scanPage)
	scanPageList = scanPageList[part.begin_page:part.end_page+1]
	defaultPageIndex=part.edited_page
	defaultPage=scanPageList[defaultPageIndex]
	defaultPageURL = sourcePath +u'/' +defaultPage
	defaultPageURL=defaultPageURL.replace(PREFIX_PATH +'static/', '')
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