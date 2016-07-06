# coding: utf-8
import codecs
import datetime
from django.core.urlresolvers import reverse, resolve
from django.http import HttpResponseRedirect,HttpResponse, Http404
from django.shortcuts import render
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import generic
from .models import *
from .forms import *
from mysite.settings import PREFIX_PATH,INACTIVE, ACTIVE, EDIT, REVIEW, REVISE, FINISH
from utils.decorator import *
from utils.crawler import get_book_info
import os
import json
import shutil

#logging config
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
# create file handler
fh = logging.FileHandler(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'log') +'/views.log')
fh.setLevel(logging.DEBUG)
# create formatter
formatter = logging.Formatter('%(asctime)s\t%(name)s\t%(levelname)s\t%(message)s')
# add formatter to fh
fh.setFormatter(formatter)
# add ch to logger
logger.addHandler(fh)

class book_list(generic.ListView):
	model = Book
	def get_queryset(self):
		return Book.objects.order_by('-bookname')

@http_response
def search_book(request, template_name):
	print request.POST
	if request.method == 'GET':
		return locals()
	if request.method == 'POST':
		if request.POST.has_key('book_ISBN'):
			book_ISBN = request.POST['book_ISBN']
			book_list = Book.objects.filter(ISBN=book_ISBN)
			if len(book_list) > 0:
				status = 'success'
				message = u'成功查詢資料'
			else:
				status = 'error'
				message = u'查無資料'
		elif request.POST.has_key('get_book'):
			book_ISBN = request.POST['get_book']
			book = Book.objects.get(ISBN=book_ISBN)
			guest = Guest.objects.get(user=request.user)
			book.guests.add(guest)
			status = 'success'
			message = u'獲取成功請到個人頁面進行email傳送'
		return locals()

@user_category_check(['manager'])
def review_document(request, book_ISBN, template_name='ebookSystem/review_document.html'):
	try:
		book = Book.objects.get(ISBN=book_ISBN)
	except:
		raise Http404("book does not exist")
	sourcePath = book.path +u'/source'
	fileList=os.listdir(sourcePath)
	fileList = sorted(fileList)
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
			book.status = ACTIVE
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

@user_category_check(['manager'])
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
			if part.book.collect_finish_part_count() == part.book.part_count:
				part.book.status = FINISH
				part.book.save()
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

@user_category_check(['manager'])
@http_response
def review_ReviseContentAction(request, id, template_name='ebookSystem/review_ReviseContentAction.html'):
	try:
		event = Event.objects.get(id=id)
		action = event.action
	except:
		raise Http404("book does not exist")
	result = action.ebook.fuzzy_string_search(string = action.content, length=10, action='-final')
	if request.method == 'GET':
		if len(result) == 1:
			status = 'success'
			message = u'成功搜尋到修政文字段落'
		elif len(result) == 0:
			status = 'error'
			message = u'搜尋不到修政文字段落，請重新輸入並多傳送些文字'
		else:
			status = 'error'
			message = u'搜尋到多處修政文字段落，請重新輸入並多傳送些文字'
		return locals()
#	if request.method == 'POST':

def detail(request, book_ISBN, template_name='ebookSystem/detail.html'):
	try:
		book = Book.objects.get(ISBN=book_ISBN)
	except:
		raise Http404("book does not exist")
	return render(request, template_name, locals())

def book_info(request, ISBN, template_name='ebookSystem/book_info.html'):
	response = {}
	result = get_book_info(ISBN)
	if result[0]:
		status = u'success'
		message = u'成功取得資料'
		response['bookname'] = result[1]
		response['author'] = result[2]
		response['house'] = result[3]
		response['date'] = result[4]
#		[bookname, author, house, date] = result[1:]
	else:
		status = u'error'
		message = u'查無資料'
	response['status'] = status
	response['message'] = message
	return HttpResponse(json.dumps(response), content_type="application/json")
#	return render(request, template_name, locals())

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

	@method_decorator(http_response)
	def get(self, request, encoding='utf-8', *args, **kwargs):
		logger.info('{}/edit\t{}'.format(request.user, resolve(request.path).namespace))
		template_name='ebookSystem/edit.html'
		user = request.user
		readmeUrl = '/ebookSystem/edit/readme/'
		try:
			book = Book.objects.get(ISBN=kwargs['book_ISBN'])
			part = EBook.objects.get(part=kwargs['part_part'],book=book)
		except: 
			raise Http404("book or part does not exist")
		[scanPageList, defaultPage, defaultPageURL] = part.get_image()
		[editContent, fileHead] = part.get_content('-edit')
		return locals()

	@method_decorator(http_response)
	def post(self, request, encoding='utf-8', *args, **kwargs):
		template_name='ebookSystem/edit.html'
		user = request.user
		readmeUrl = '/ebookSystem/edit/readme/'
		response = {}
		try:
			book = Book.objects.get(ISBN=kwargs['book_ISBN'])
			part = EBook.objects.get(part=kwargs['part_part'],book=book)
		except:
			raise Http404("book or part does not exist")
		[scanPageList, defaultPage, defaultPageURL] = part.get_image()
		editForm = EditForm(request.POST)
		if request.POST.has_key('save'):
			content = request.POST['content']
			[finishContent, editContent] = part.split_content(content)
			if finishContent == '' or editContent == '':
				status = 'error'
				message = u'標記位置不可在首行或末行'
				return locals()
			part.set_content(finish_content=finishContent, edit_content=editContent)
#			part.set_content(finish_content='', edit_content=content)
			part.edited_page=int(request.POST['page'])
			part.save()
			[scanPageList, defaultPage, defaultPageURL] = part.get_image()
			[editContent, fileHead] = part.get_content('-edit')
			status = 'success'
			message = u'您上次儲存時間為：{0}，請定時存檔喔~'.format(timezone.now())
		elif request.POST.has_key('close'):
			status = 'success'
			message = u'關閉無儲存資料'
			redirect_to = reverse('account:profile')
		elif request.POST.has_key('finish'):
			content = request.POST['content']
			part.set_content(finish_content=content, edit_content='')
			part.edited_page = int(request.POST['page'])
			part.status = REVIEW
			part.finish_date = timezone.now()
			part.save()
			redirect_to = reverse('account:profile')
			status = 'success'
			message = u'完成文件校對，將進入審核'
		return locals()

def readme(request, template_name):
	template_name = resolve(request.path).namespace +'/' +template_name +'_readme.html'
	return render(request, template_name, locals())