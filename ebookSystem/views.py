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
from utils.analysis import *
from utils.crawler import *
from utils.decorator import *
import os
import json
import shutil
import uuid
from django.views.decorators.cache import cache_control


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
def mathml(request, template_name='ebookSystem/mathml_demo.html'):
	if request.method == 'POST':
		if request.POST.has_key('set'):
			cache.set(request.user.username, {'mathml':request.POST['content']}, 600)
			status = u'success'
			message = u'成功暫存內容'
		if request.POST.has_key('get'):
			if not cache.has_key(request.user.username):
				status = u'error'
				message = u'server無資料'
				return locals()
			math_content = cache.get(request.user.username)['mathml']
			extra_list = ['math_content']
			status = u'success'
			message = u'成功獲取內容'
		return locals()
	if request.method == 'GET':
		status = u'success'
		message = u'成功獲取內容'
		return locals()

@http_response
def search_book(request, template_name):
	if request.method == 'GET':
		return locals()
	if request.method == 'POST':
		if request.POST.has_key('book_ISBN'):
			ISBN = request.POST['book_ISBN']
			try:
				search_book = Book.objects.get(ISBN=ISBN)
				status = 'success'
				message = u'成功查詢指定ISBN文件'
			except:
				status = 'error'
				message = u'查無指定ISBN文件'
		if request.POST.has_key('get_book'):
			from django.core.mail import EmailMessage
			ISBN = request.POST['get_book']
			emailBook = Book.objects.get(ISBN=ISBN)
			subject = u'[文件] {}'.format(emailBook.book_info.bookname)
			body = u'新愛的{0}您好：\n'.format(request.user.username)
			email = EmailMessage(subject=subject, body=body, from_email=SERVICE, to=[request.user.email])
			attach_file_path = emailBook.zip('test')
			if attach_file_path == '':
				status = 'error'
				message = u'附加文件失敗'
				os.remove(attach_file_path)
				return locals()
			email.attach_file(attach_file_path)
			email.send(fail_silently=False)
			status = 'success'
			message = u'已寄送到您的電子信箱'
			os.remove(attach_file_path)
		return locals()

@user_category_check(['manager'])
@http_response
def review_document(request, book_ISBN, template_name='ebookSystem/review_document.html'):
#	status = 'error'
#	message= 'referenced before assignment'
	try:
		book = Book.objects.get(ISBN=book_ISBN)
	except:
		raise Http404("book does not exist")
	events = Event.objects.filter(content_type__model='book', object_id=book.ISBN, status=Event.STATUS['review'])
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
			book.status = book.STATUS['active']
			shutil.rmtree(org_path)
			book.save()
			status = 'success'
			message = u'審核通過文件'
			for event in events:
				event.response(status=status, message=message, user=request.user)
		if request.POST['review'] == 'error':
			shutil.rmtree(book.path)
			shutil.rmtree(org_path)
			book.delete()
			status = 'success'
			message = u'審核退回文件'
			for event in events:
				event.response(status='error', message=request.POST['reason'], user=request.user)
		redirect_to = reverse('manager:event_list', kwargs={'action':'book' })
		return locals()

@user_category_check(['manager'])
@http_response
def analyze_part(request, ISBN_part, template_name='ebookSystem/analyze_part.html'):
	try:
		part = EBook.objects.get(ISBN_part=ISBN_part)
	except:
		raise Http404("book does not exist")
	if not os.path.exists(part.get_path('-manual_clean')):
		shutil.copy2(part.get_path('-sc'), part.get_path('-manual_clean'))
	if request.method == 'GET':
		[len_block, same_character, src_count, dst_count] = diff(part.get_path(), part.get_path('-finish'))
		ed = edit_distance(part.get_path(), part.get_path('-finish'))
		delete_count = src_count -same_character
		insert_count = dst_count -same_character
		diff_count = dst_count -src_count
		lc_dict = last_character(part.get_path('-manual_clean'))
		lc_list = lc_dict.items()
		re_dict = find_repeat(part.get_path('-manual_clean'))
		re_list = re_dict.items()
		status = u'success'
		message = u'分析文件'
		return locals()
	if request.method == 'POST':
		if request.POST.has_key('download'):
			download_path = part.get_path('-manual_clean')
			download_filename = u'part{0}-manual_clean.html'.format(part.part)
			status = u'success'
			message = u'下載'
			return locals()
		elif request.POST.has_key('upload') and request.FILES.has_key('fileObject'):
			with open(part.get_path('-manual_clean'), 'wb+') as dst:
				for chunk in request.FILES['fileObject'].chunks():
					dst.write(chunk)
			[len_block, same_character, src_count, dst_count] = diff(part.get_path(), part.get_path('-finish'))
			ed = edit_distance(part.get_path(), part.get_path('-finish'))
			delete_count = src_count -same_character
			insert_count = dst_count -same_character
			diff_count = dst_count -src_count
			lc_dict = last_character(part.get_path('-manual_clean'))
			lc_list = lc_dict.items()
			re_dict = find_repeat(part.get_path('-manual_clean'))
			re_list = re_dict.items()
			status = u'success'
			message = u'檔案成功更新'
			return locals()
		elif request.POST.has_key('finish'):
			part.status = part.STATUS['sc_active']
			part.save()
			status = u'success'
			message = u'完成'
			redirect_to = reverse('account:an_service')
			return locals()

@user_category_check(['manager'])
@http_response
def review_part(request, ISBN_part, template_name='ebookSystem/review_part.html'):
	try:
		part = EBook.objects.get(ISBN_part=ISBN_part)
	except:
		raise Http404("book does not exist")
	events = Event.objects.filter(content_type__model='ebook', object_id=part.ISBN_part, status=Event.STATUS['review'])
	part.clean_tag()
	html_url = part.get_html()
	if request.method == 'GET':
		[len_block, same_character, src_count, dst_count] = diff(part.get_path(), part.get_path('-finish'))
		ed = edit_distance(part.get_path(), part.get_path('-finish'))
		delete_count = src_count -same_character
		insert_count = dst_count -same_character
		diff_count = dst_count -src_count
		return locals()
	if request.method == 'POST':
		if request.POST['review'] == 'success':
			part.status = part.STATUS['finish']
			month_day = datetime.date(year=datetime.date.today().year, month=datetime.date.today().month, day=1)
			if len(events) > 0:
				try:
					month_ServiceHours = ServiceHours.objects.get(user=events[0].creater, date=month_day)
				except:
					month_ServiceHours = ServiceHours.objects.create(user=events[0].creater, date=month_day)
				part.serviceHours = month_ServiceHours
				month_ServiceHours.service_hours = month_ServiceHours.service_hours +part.service_hours
				month_ServiceHours.save()
			import shutil
			shutil.copy2(part.get_path('-clean'), part.get_path('-sc'))
			part.book.save()
			part.save()
			if part.book.collect_finish_part_count() == part.book.part_count:
				part.book.status = part.book.STATUS['finish']
			status = 'success'
			message = u'審核通過文件'
			for event in events:
				event.response(status=status, message=message, user=request.user)
		if request.POST['review'] == 'error':
			part.status = part.STATUS['edit']
			part.finish_date = None
			part.load_full_content()
			part.save()
			status = 'success'
			message = u'審核退回文件'
			for event in events:
				event.response(status='error', message=request.POST['reason'], user=request.user)
		os.remove(BASE_DIR +'/static/' +html_url)
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
		event = Event.objects.get(content_type__model='applydocumentaction', object_id=action.id, status=Event.STATUS['review'])
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
		newBook.owner = user
		if request.POST.has_key('designate'):
			newBook.is_private = True
		newBook.save()
		newBook.create_EBook()
		Event.objects.create(creater=event.creater, action=newBook)
		redirect_to = reverse('manager:event_list', kwargs={'action':'applydocumentaction' })
		status = 'success'
		message = u'成功建立並上傳文件'
		event.response(status=status, message=message, user=request.user)
		return locals()

@user_category_check(['user'])
@http_response
def detail(request, book_ISBN, template_name='ebookSystem/detail.html'):
	try:
		book = Book.objects.get(ISBN=book_ISBN)
	except:
		raise Http404("book does not exist")
	if request.method == 'POST':
		if request.POST.has_key('emailEBook'):
			from django.core.mail import EmailMessage
			from mysite.settings import SERVICE
			ISBN_part = request.POST.get('emailEBook')
			emailEBook = EBook.objects.get(ISBN_part = ISBN_part)
			subject = u'[文件] {0}-part{1}'.format(emailEBook.book.book_info.bookname, emailEBook.part)
			body = u'新愛的{0}您好：\n'.format(request.user.username)
			email = EmailMessage(subject=subject, body=body, from_email=SERVICE, to=[request.user.email])
			attach_file_path = emailEBook.zip('test')
			if attach_file_path == '':
				status = 'error'
				message = u'附加文件失敗'
				os.remove(attach_file_path)
				return locals()
			email.attach_file(attach_file_path)
			email.send(fail_silently=False)
			status = 'success'
			message = u'已寄送到您的電子信箱'
			os.remove(attach_file_path)
		return locals()
	if request.method == 'GET':
		return locals()

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
	if not request.POST.has_key('online'):
		response['status'] = 'error'
		response['message'] = ''
		return HttpResponse(json.dumps(response), content_type="application/json")
	delta = timezone.now() - user.online
	if delta.seconds < 50:
		response['status'] = u'error'
		response['message'] = u'您有其他編輯正進行'
		return HttpResponse(json.dumps(response), content_type="application/json")
	user.online = timezone.now()
	user.save()
	part = EBook.objects.get(ISBN_part=ISBN_part)
	part.service_hours = part.service_hours+1
	part.save()
	response['status'] = u'success'
	response['message'] = part.service_hours
	return HttpResponse(json.dumps(response), content_type="application/json")

class editView(generic.View):

	@cache_control(no_store=True, no_cache=True, max_age=0)
	@method_decorator(http_response)
	def get(self, request, encoding='utf-8', *args, **kwargs):
		logger.info('{}/edit\t{}'.format(request.user, resolve(request.path).namespace))
		template_name='ebookSystem/edit.html'
		try:
			part = EBook.objects.get(ISBN_part=kwargs['ISBN_part'])
		except: 
			raise Http404("book or part does not exist")
		postToken = uuid.uuid1().hex
		request.session['postToken'] = postToken
		[scanPageList, defaultPageURL] = part.get_image(request.user)
		[editContent, fileHead] = part.get_content('-edit')
		return locals()

	@cache_control(no_store=True, no_cache=True, max_age=0)
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
		content = request.POST['content']
		Token = request.session.get('postToken',default=None)
		userToken = request.POST['postToken']
		print ("Token %d",Token)
		print (" userToken %d",userToken)
		if  userToken !=Token:
			raise Http404("請勿重覆傳送")
		if request.POST.has_key('save'):
			[finishContent, editContent] = part.split_content(content)
			if finishContent == '' or editContent == '':
				status = 'error'
				message = u'標記位置不可在首行或末行'
				[scanPageList, defaultPageURL] = part.get_image(request.user)
				[editContent, fileHead] = part.get_content('-edit')
				return locals()
			part.set_content(finish_content=finishContent, edit_content=editContent)
			part.edited_page=int(request.POST['page'])
			part.save()
			status = 'success'
			message = u'您上次儲存時間為：{0}，請定時存檔喔~'.format(timezone.now())
		elif request.POST.has_key('close'):
			status = 'success'
			message = u'關閉無儲存資料'
			redirect_to = reverse('account:profile')
		elif request.POST.has_key('finish'):
			part.set_content(finish_content=content, edit_content='')
			part.edited_page = part.book.page_per_part -1
			part.status = part.STATUS['review']
			part.save()
			redirect_to = reverse('account:profile')
			status = 'success'
			message = u'完成文件校對，將進入審核'
			events = Event.objects.filter(content_type__model='ebook', object_id=part.ISBN_part, status=Event.STATUS['review'])
			if len(events) == 0:
				event = Event.objects.create(creater=user, action=part)
		elif request.POST.has_key('load'):
			part.load_full_content()
			status = 'success'
			message = u'成功載入全部文件內容'
		[scanPageList, defaultPageURL] = part.get_image(request.user)
		[editContent, fileHead] = part.get_content('-edit')
		del request.session['postToken']
		postToken = uuid.uuid1().hex
		request.session['postToken'] = postToken
		print request.session.get('postToken',default=None)
		return locals()

@http_response
def full_edit(request, ISBN_part, template_name='ebookSystem/full_edit.html'):
	try:
		part = EBook.objects.get(ISBN_part=ISBN_part)
	except:
		raise Http404("book does not exist")
	[scanPageList, defaultPageURL] = part.get_image(request.user)
	[editContent, fileHead] = part.get_content('-sc')
	if request.method == 'POST':
		with codecs.open(part.get_path('-sc'), 'w', encoding='utf-8') as scFile:
			scFile.write(u'\ufeff' +request.POST['content'])
		return locals()
	if request.method == 'GET':
		return locals()

@http_response
def special_content(request, ISBN_part, template_name='ebookSystem/special_content.html'):
	try:
		part = EBook.objects.get(ISBN_part=ISBN_part)
	except:
		raise Http404("book does not exist")
	sc_list = part.specialcontent_set.all().order_by('tag_id')
	if request.method == 'POST':
		if request.POST.has_key('rebuild'):
			part.delete_SpecialContent()
			part.create_SpecialContent()
		if request.POST.has_key('full_write'):
			for sc in part.specialcontent_set.all():
				sc.write_to_file()
		if request.POST.has_key('finish'):
			if part.is_sc_rebuild:
				status = u'error'
				message = u'請先進行特殊內容檢查'
				return locals()
			part.status = part.STATUS['sc_finish']
			part.save()
			redirect_to = reverse('account:sc_service')
		if request.POST.has_key('write'):
			sc = SpecialContent.objects.get(id=request.POST['write'])
			sc.write_to_file()
		status = u'success'
		message = u'操作動作成功'
		return locals()
	if request.method == 'GET':
		return locals()
@http_response
def edit_SpecialContent(request, id, type):
	try:
		sc = SpecialContent.objects.get(id=id)
	except: 
		raise Http404("special content does not exist")
	part = sc.ebook
	page = sc.page
	water_path = BASE_DIR +u'/static/ebookSystem/document/{0}/source/{1}'.format(part.book.book_info.ISBN, request.user.username)
	[scanPageList, defaultPageURL] = part.get_image(request.user)
	sc_list = list(SpecialContent.objects.filter(ebook=part).order_by('tag_id'))
	total_count = len(sc_list)
	current_count = sc_list.index(sc)
	try:
		next_sc = sc_list[current_count+1]
	except:
		next_sc = None
	if current_count == 0:
		previous_sc = None
	else:
		previous_sc = sc_list[current_count-1]
	if page == 0:
		show_page = 0
		scanPageList = scanPageList[page:page+2]
		default_page_url = water_path +u'/' +scanPageList[0]
	elif page == part.book.page_per_part-1:
		show_page = 1
		scanPageList = scanPageList[page-1:page+1]
		default_page_url = water_path +u'/' +scanPageList[1]
	else:
		show_page = 1
		scanPageList = scanPageList[page-1:page+2]
		default_page_url = water_path +u'/' +scanPageList[1]
	default_page_url=default_page_url.replace(BASE_DIR +'/static/', '')
	from bs4 import BeautifulSoup
	if type == 'mathml':
		math_tag = BeautifulSoup(sc.content, 'lxml').find('math')
		editContent = str(math_tag)
	elif type == 'image':
		img_tag = BeautifulSoup(sc.content, 'lxml').find('img')
		image_path = sc.ebook.book.path +'/OCR/image/' +sc.id +'.jpg'
		image_public_path = sc.ebook.get_path('public') +'/OCR/image/' +sc.id +'.jpg'
		preview_image_url = image_public_path.replace(BASE_DIR +'/static/', '')
		editContent = img_tag['alt']
	elif type == 'unknown':
		editContent = sc.content
	template_name = 'ebookSystem/edit_{0}.html'.format(type)
	if request.method == 'POST':
		if request.POST.has_key('save') or request.POST.has_key('write'):
			if type == 'image':
				img_tag['src'] = 'image/' +sc.id +'.jpg'
				img_tag['alt'] = request.POST['alt']
				sc.content = u'<p id="{0}">'.format(sc.tag_id) +img_tag.prettify(formatter='html') +u'</p>'
				if not os.path.exists(os.path.dirname(image_path)):
					os.makedirs(os.path.dirname(image_path), 0770)
				if not os.path.exists(os.path.dirname(image_public_path)):
					os.makedirs(os.path.dirname(image_public_path), 0770)
				try:
					with open(image_path, 'wb+') as dst:
						for chunk in request.FILES['imageFile'].chunks():
							dst.write(chunk)
					shutil.copy2(image_path, image_public_path)
				except:
					pass
			elif type == 'mathml':
				math_tag = BeautifulSoup(request.POST['content'], 'lxml').find('math')
				sc.content = u'<p id="{0}">'.format(sc.tag_id) +math_tag.prettify(formatter='html') +u'</p>'
			elif type == 'unknown':
				sc.content = request.POST['content']
			sc.save()
			status = u'success'
			message = u'暫存'
		if request.POST.has_key('write'):
			sc.write_to_file()
			status = u'success'
			message = u'寫入'
			redirect_to = reverse('ebookSystem:special_content', kwargs={'ISBN_part':part.ISBN_part})
		if request.POST.has_key('upload'):
			if type == 'image':
				dirname = sc.ebook.book.path +'/OCR/image/'
				if not os.path.exists(dirname):
					os.makedirs(dirname, 0770)
				path = dirname +sc.id +'.jpg'
				with open(path, 'wb+') as dst:
					for chunk in request.FILES['imageFile'].chunks():
						dst.write(chunk)
			status = u'success'
			message = u'上傳'
		if request.POST.has_key('download'):
			if type == 'image':
				download_path = part.book.path +'/source/' +request.POST['download']
				download_filename = request.POST['download']
			status = u'success'
			message = u'下載'
		return locals()
	if request.method == 'GET':
		return locals()

#def readme(request, template_name):
#	template_name = resolve(request.path).namespace +'/' +template_name +'_readme.html'
#	return render(request, template_name, locals())