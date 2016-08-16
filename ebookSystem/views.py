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
from genericUser.models import Event, ServiceHours
from mysite.settings import BASE_DIR
from utils.decorator import *
from utils.crawler import *
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
		return Book.objects.order_by('-ISBN')

@http_response
def search_book(request, template_name):
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
			book.owners.add(guest)
			status = 'success'
			message = u'獲取成功請到個人頁面進行email傳送'
			redirect_to = reverse('guest:profile')
		return locals()

@user_category_check(['manager'])
@http_response
def review_document(request, book_ISBN, template_name='ebookSystem/review_document.html'):
	try:
		book = Book.objects.get(ISBN=book_ISBN)
		event = Event.objects.get(content_type__model='book', object_id=book.ISBN)
	except:
		raise Http404("book does not exist")
	org_path = BASE_DIR +u'/static/ebookSystem/document/{0}/source/{1}'.format(book.book_info.ISBN,"org")
	source_path = book.path +u'/source'
	scanPageList=[]
	for ebook in book.ebook_set.all():
		scanPageList = scanPageList + ebook.get_org_image(request.user)[0]
	defaultPageURL = org_path +u'/' +scanPageList[0]
	defaultPageURL=defaultPageURL.replace(BASE_DIR +'/static/', '')
	if request.method == 'GET':
		return locals()
	if request.method == 'POST':
		if request.POST['review'] == 'success':
			if book.status == book.STATUS['inactive']:
				book.status = book.STATUS['active']
			elif book.status == book.STATUS['indesignate']:
				book.status = book.STATUS['designate']
			book.save()
			shutil.rmtree(org_path)
			status = 'success'
			message = u'審核通過文件'
			event.response(status=status, message=message, user=request.user)
		if request.POST['review'] == 'error':
			shutil.rmtree(book.path)
			book.delete()
			shutil.rmtree(org_path)
			status = 'success'
			message = u'審核退回文件'
			event.response(status='error', message=request.POST['reason'], user=request.user)
		redirect_to = reverse('manager:event_list', kwargs={'action':'book' })
		return locals()

@user_category_check(['manager'])
@http_response
def review_part(request, ISBN_part, template_name='ebookSystem/review_part.html'):
	try:
		part = EBook.objects.get(ISBN_part=ISBN_part)
		event = Event.objects.get(content_type__model='ebook', object_id=part.ISBN_part)
	except:
		raise Http404("book does not exist")
	[content, fileHead] = part.get_content('-finish')
	if request.method == 'GET':
		return locals()
	if request.method == 'POST':
		if request.POST['review'] == 'success':
			part.status = part.STATUS['finish']
			if part.book.collect_finish_part_count() == part.book.part_count:
				part.book.status = part.book.STATUS['finish']
				part.book.save()
			month_day = datetime.date(year=datetime.date.today().year, month=datetime.date.today().month, day=1)
			try:
				month_ServiceHours = ServiceHours.objects.get(user=request.user, date=month_day)
			except:
				month_ServiceHours = ServiceHours.objects.create(user=request.user, date=month_day)
			part.serviceHours = month_ServiceHours
			part.save()
			import shutil
			shutil.copyfile(part.get_path('-finish'), part.get_path('-final'))
			status = 'success'
			message = u'審核通過文件'
			event.response(status=status, message=message, user=request.user)
		if request.POST['review'] == 'error':
			part.status = part.STATUS['revise']
			part.save()
			status = 'success'
			message = u'審核退回文件'
			event.response(status='error', message=request.POST['reason'], user=request.user)
		redirect_to = reverse('manager:event_list', kwargs={'action':'ebook' })
		return locals()

@user_category_check(['manager'])
@http_response
def review_ReviseContentAction(request, id, template_name='ebookSystem/review_ReviseContentAction.html'):
	try:
		action = ReviseContentAction.objects.get(id=id)
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
	if request.method == 'POST':
		return locals()

@user_category_check(['manager'])
@http_response
def review_ApplyDocumentAction(request, id, template_name='ebookSystem/review_ApplyDocumentAction.html'):
	from utils.uploadFile import handle_uploaded_file
	user = request.user
	try:
		action = ApplyDocumentAction.objects.get(id=id)
		event = Event.objects.get(content_type__model='applydocumentaction', object_id=action.id)
	except:
		raise Http404("ApplyDocumentAction does not exist")
	if request.method == 'GET':
		return locals()
	if request.method == 'POST':
		uploadPath = BASE_DIR +u'/file/ebookSystem/document/{0}'.format(action.book_info.ISBN)
		if os.path.exists(uploadPath):
			status = 'error'
			message = u'文件已存在'
			return locals()
		[status, message] = handle_uploaded_file(uploadPath, request.FILES['fileObject'])
		uploadFilePath = os.path.join(uploadPath, request.FILES['fileObject'].name)
		try:
			from zipfile import ZipFile
			with ZipFile(uploadFilePath, 'r') as uploadFile:
				uploadFile.testzip()
				uploadFile.extractall(uploadPath)
		except:
				shutil.rmtree(uploadPath)
				status = 'error'
				message = u'非正確ZIP文件'
				return locals()
		newBook = Book(book_info=action.book_info, ISBN=action.book_info.ISBN)
		newBook.path = uploadPath
		if not newBook.validate_folder():
			shutil.rmtree(uploadPath)
			status = 'error'
			message = u'上傳壓縮文件結構錯誤，詳細結構請參考說明頁面'
			return locals()
		newBook.scaner = user
		guest = Guest.objects.get(user=event.creater)
		newBook.owners.add(guest)
		if request.POST.has_key('designate'):
			newBook.status = newBook.STATUS['indesignate']
		newBook.save()
		newBook.create_EBook()
		Event.objects.create(creater=event.creater, action=newBook)
		redirect_to = reverse('manager:event_list', kwargs={'action':'applydocumentaction' })
		status = 'success'
		message = u'成功建立並上傳文件'
		event.response(status=status, message=message, user=request.user)
		return locals()

def detail(request, book_ISBN, template_name='ebookSystem/detail.html'):
	try:
		book = Book.objects.get(ISBN=book_ISBN)
	except:
		raise Http404("book does not exist")
	return render(request, template_name, locals())

@http_response
def book_info(request, ISBN, template_name='ebookSystem/book_info.html'):
	if len(ISBN) == 10 and not ISBN10_check(ISBN):
		status = u'error'
		message = u'ISBN10碼錯誤'
		return locals()
	if len(ISBN) == 13 and not ISBN13_check(ISBN):
		status = u'error'
		message = u'ISBN13碼錯誤'
		return locals()
	if len(ISBN) == 10:
		ISBN = ISBN10_to_ISBN13(ISBN)
	[status, bookname, author, house, date] = get_book_info(ISBN)
	if status == 'success':
		message = u'成功取得資料'
	else:
		message = u'查無資料'
	extra_list = ['bookname', 'author', 'house', 'date', 'ISBN']
	return locals()

def edit_ajax(request, ISBN_part, *args, **kwargs):
	user = request.user
	response={}
	response = {}
	if not hasattr(request.user, 'online'):
		response['status'] = u'error'
		response['message'] = u'已登出'
	if 'online' in request.POST:
		delta = timezone.now() - user.online
		if delta.seconds < 50:
			response['status'] = u'error'
			response['message'] = u'您有其他編輯正進行'
		else:
			user.online = timezone.now()
			user.save()
			part = EBook.objects.get(ISBN_part=ISBN_part)
			part.service_hours = part.service_hours+1
			part.save()
			response['status'] = u'success'
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
		readme_url = request.path +'readme/'
		try:
			part = EBook.objects.get(ISBN_part=kwargs['ISBN_part'])
		except: 
			raise Http404("book or part does not exist")
		[scanPageList, defaultPageURL] = part.get_image(request.user)
		[editContent, fileHead] = part.get_content('-edit')
		return locals()

	@method_decorator(http_response)
	def post(self, request, encoding='utf-8', *args, **kwargs):
		template_name='ebookSystem/edit.html'
		user = request.user
		readme_url = request.path +'readme/'
		response = {}
		try:
			part = EBook.objects.get(ISBN_part=kwargs['ISBN_part'])
		except:
			raise Http404("book or part does not exist")
		[scanPageList, defaultPageURL] = part.get_image(request.user)
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
			[scanPageList, defaultPageURL] = part.get_image(request.user)
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
			part.status = part.STATUS['review']
			part.finish_date = timezone.now()
			part.save()
			redirect_to = reverse('account:profile')
			status = 'success'
			message = u'完成文件校對，將進入審核'
			event = Event.objects.create(creater=user, action=part)
		return locals()

def readme(request, template_name):
	template_name = resolve(request.path).namespace +'/' +template_name +'_readme.html'
	return render(request, template_name, locals())