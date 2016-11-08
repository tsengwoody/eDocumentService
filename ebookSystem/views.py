# coding: utf-8
import codecs
import datetime
from zipfile import ZipFile
from django.core.urlresolvers import reverse, resolve
from django.http import HttpResponseRedirect,HttpResponse, Http404
from django.shortcuts import render
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import generic
from .models import *
from .forms import *
from genericUser.models import Event, ServiceHours
from mysite.settings import BASE_DIR, SERVICE
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

#class book_list(generic.ListView):
#	model = Book
#	def get_queryset(self):
#		return Book.objects.order_by('-ISBN')

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

@user_category_check(['manager'])
@http_response
def book_list(request, template_name='ebookSystem/book_list.html'):
	object_list = Book.objects.all()
	if request.method == 'POST':
		return locals()
	if request.method == 'GET':
		return locals()

@http_response
def search_book(request, template_name):
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
		if request.POST.has_key('email'):
			from django.core.mail import EmailMessage
			getBook = Book.objects.get(ISBN=request.POST['email'])
			attach_file_path = getBook.zip(request.user, 'test')
			if not attach_file_path:
				status = 'error'
				message = u'準備文件失敗'
				return locals()
			subject = u'[文件] {0}'.format(getBook)
			body = u'新愛的{0}您好：\n'.format(request.user.username)
			email = EmailMessage(subject=subject, body=body, from_email=SERVICE, to=[request.user.email])
			email.attach_file(attach_file_path)
			email.send(fail_silently=False)
			status = 'success'
			message = u'已寄送到您的電子信箱'
			os.remove(attach_file_path)
		if request.POST.has_key('download'):
			getBook = Book.objects.get(ISBN=request.POST['download'])
			attach_file_path = getBook.zip(request.user, 'test')
			if not attach_file_path:
				status = 'error'
				message = u'準備文件失敗'
				return locals()
			download_path = attach_file_path
			download_filename = os.path.basename(attach_file_path)
		return locals()
	if request.method == 'GET':
		return locals()

@user_category_check(['manager'])
@http_response
def review_document(request, book_ISBN, template_name='ebookSystem/review_document.html'):
	try:
		book = Book.objects.get(ISBN=book_ISBN)
	except:
		raise Http404("book does not exist")
	events = Event.objects.filter(content_type__model='book', object_id=book.ISBN, status=Event.STATUS['review'])
	org_path = BASE_DIR +u'/static/ebookSystem/document/{0}/source/{1}'.format(book.book_info.ISBN,"org")
	source_path = book.path +u'/source'
	[scanPageList, defaultPageURL] = book.get_org_image(request.user)
	if request.method == 'GET':
		return locals()
	if request.method == 'POST':
		if request.POST['review'] == 'success':
			book.create_EBook()
			for part in book.ebook_set.all():
				part.change_status(1, 'active')
			shutil.rmtree(org_path)
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
	if request.method == 'GET':
		[len_block, same_character, src_count, dst_count] = diff(part.get_path(), part.get_path('-finish'))
		ed = edit_distance(part.get_path(), part.get_path('-finish'))
		delete_count = src_count -same_character
		insert_count = dst_count -same_character
		diff_count = dst_count -src_count
		if os.path.exists(part.get_path('-an')):
			lc_dict = last_character(part.get_path('-an'))
			lc_list = lc_dict.items()
			re_dict = find_repeat(part.get_path('-an'))
			re_list = re_dict.items()
		else:
			lc_dict = last_character(part.get_path('-clean'))
			lc_list = lc_dict.items()
			re_dict = find_repeat(part.get_path('-clean'))
			re_list = re_dict.items()
		status = u'success'
		message = u'分析文件'
		return locals()
	if request.method == 'POST':
		if request.POST.has_key('download'):
			download_path = part.get_path('-an')
			download_filename = u'part{0}-an.html'.format(part.part)
			status = u'success'
			message = u'下載'
			return locals()
		elif request.POST.has_key('upload') and request.FILES.has_key('fileObject'):
			with open(part.get_path('-an'), 'wb+') as dst:
				for chunk in request.FILES['fileObject'].chunks():
					dst.write(chunk)
			[len_block, same_character, src_count, dst_count] = diff(part.get_path(), part.get_path('-finish'))
			ed = edit_distance(part.get_path(), part.get_path('-finish'))
			delete_count = src_count -same_character
			insert_count = dst_count -same_character
			diff_count = dst_count -src_count
			if os.path.exists(part.get_path('-an')):
				lc_dict = last_character(part.get_path('-an'))
				lc_list = lc_dict.items()
				re_dict = find_repeat(part.get_path('-an'))
				re_list = re_dict.items()
			else:
				lc_dict = last_character(part.get_path('-clean'))
				lc_list = lc_dict.items()
				re_dict = find_repeat(part.get_path('-clean'))
				re_list = re_dict.items()
			status = u'success'
			message = u'檔案成功更新'
			return locals()
		elif request.POST.has_key('finish'):
			part.change_status(1, 'an_finish', request.user)
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
	if request.method == 'GET':
		[len_block, same_character, src_count, dst_count] = diff(part.get_path(), part.get_path('-finish'))
		ed = edit_distance(part.get_path(), part.get_path('-finish'))
		delete_count = src_count -same_character
		insert_count = dst_count -same_character
		diff_count = dst_count -src_count
		return locals()
	if request.method == 'POST':
		if request.POST['review'] == 'success':
			part.change_status(1, 'finish')
			status = 'success'
			message = u'審核通過文件'
			for event in events:
				event.response(status=status, message=message, user=request.user)
		if request.POST['review'] == 'error':
			part.change_status(-1, 'edit')
			status = 'success'
			message = u'審核退回文件'
			for event in events:
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

@user_category_check(['advanced_editor'])
@http_response
def review_ApplyDocumentAction(request, id, template_name='ebookSystem/review_ApplyDocumentAction.html'):
	from utils.uploadFile import handle_uploaded_file
	BookInfoForm = modelform_factory(BookInfo, fields=('bookname', 'author', 'house', 'date'))
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
			with ZipFile(uploadFilePath, 'r') as uploadFile:
				uploadFile.testzip()
				uploadFile.extractall(uploadPath)
		except:
				shutil.rmtree(uploadPath)
				status = 'error'
				message = u'非正確ZIP文件'
				return locals()
		newBook = Book(book_info=action.book_info, ISBN=action.book_info.ISBN, path=uploadPath)
		if not newBook.validate_folder():
			shutil.rmtree(uploadPath)
			status = 'error'
			message = u'上傳壓縮文件結構錯誤，詳細結構請參考說明頁面'
			return locals()
		newBook.set_page_count()
		newBook.scaner = request.user
		newBook.owner = request.user
		if request.POST.has_key('designate'):
			newBook.is_private = True
		newBook.save()
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
		if request.POST.has_key('email'):
			from django.core.mail import EmailMessage
			getPart = EBook.objects.get(ISBN_part=request.POST['email'])
			attach_file_path = getPart.zip(request.user, 'test')
			if not attach_file_path:
				status = 'error'
				message = u'準備文件失敗'
				return locals()
			subject = u'[文件] {0}'.format(getPart)
			body = u'新愛的{0}您好：\n'.format(request.user.username)
			email = EmailMessage(subject=subject, body=body, from_email=SERVICE, to=[request.user.email])
			email.attach_file(attach_file_path)
			email.send(fail_silently=False)
			status = 'success'
			message = u'已寄送到您的電子信箱'
			os.remove(attach_file_path)
		if request.POST.has_key('download'):
			getPart = EBook.objects.get(ISBN_part=request.POST['download'])
			attach_file_path = getPart.zip(request.user, 'test')
			if not attach_file_path:
				status = 'error'
				message = u'準備文件失敗'
				return locals()
			download_path = attach_file_path
			download_filename = os.path.basename(attach_file_path)
			status = u'success'
			message = u'下載'
		return locals()
	if request.method == 'GET':
		return locals()

@user_category_check(['superuser'])
@http_response
def detail_manager(request, book_ISBN, template_name='ebookSystem/detail_manager.html'):
	try:
		book = Book.objects.get(ISBN=book_ISBN)
	except:
		raise Http404("book does not exist")
	if request.method == 'POST':
		if request.POST.has_key('view'):
			getPart = EBook.objects.get(ISBN_part=request.POST['view'])
			attach_file_path = getPart.get_file()
			if not attach_file_path:
				status = 'error'
				message = u'準備文件失敗'
				return locals()
			download_path = attach_file_path
			download_filename = os.path.basename(attach_file_path)
		if request.POST.has_key('view_se'):
			getPart = EBook.objects.get(ISBN_part=request.POST['view_se'])
			attach_file_path = getPart.replace()
			if not attach_file_path:
				status = 'error'
				message = u'準備文件失敗'
				return locals()
			download_path = attach_file_path
			download_filename = os.path.basename(attach_file_path)
		return locals()
	if request.method == 'GET':
		return locals()

@user_category_check(['superuser'])
@http_response
def edit_log(request, ISBN_part, template_name='ebookSystem/edit_log.html'):
	try:
		part = EBook.objects.get(ISBN_part=ISBN_part)
	except:
		raise Http404("ebook does not exist")
	if request.method == 'POST':
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
	if not getattr(request.user, 'has_editor', None):
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
	try:
		editRecord = EditRecord.objects.get(part=part, category='based', number_of_times=part.number_of_times)
	except:
		editRecord = EditRecord.objects.create(part=part, category='based', number_of_times=part.number_of_times)
	order = len(EditLog.objects.filter(edit_record=editRecord))
	EditLog.objects.create(edit_record=editRecord, user=request.user, time=timezone.now(), order=order, edit_count=int(request.POST['online']))
	response['status'] = u'success'
	response['message'] = part.service_hours
	return HttpResponse(json.dumps(response), content_type="application/json")

@cache_control(no_store=True, no_cache=True, max_age=0)
@user_category_check('editor')
@http_response
def edit(request, template_name='ebookSystem/edit.html', encoding='utf-8', *args, **kwargs):
	logger.info('{}/edit\t{}'.format(request.user, resolve(request.path).namespace))
	try:
		part = EBook.objects.get(ISBN_part=kwargs['ISBN_part'])
	except: 
		raise Http404("book or part does not exist")
	if not part.editor == request.user:
		status = u'error'
		message = u'您非本文件之校對者！'
#		permission_denied = True
		redirect_to = reverse('account:service')
		return locals()
	[scanPageList, defaultPageURL] = part.get_image(request.user)
	editContent = part.get_content('-edit')
	if request.method == 'POST':
		Token = request.session.get('postToken',default=None)
		userToken = request.POST['postToken']
		print ("Token %d",Token)
		print (" userToken %d",userToken)
		if  userToken !=Token:
			raise Http404("請勿重覆傳送")
		content = request.POST['content']
		if request.POST.has_key('save'):
			[finishContent, editContent] = part.split_content(content)
			if finishContent == '' or editContent == '':
				status = 'error'
				message = u'標記位置不可在首行或末行'
				return locals()
			part.set_content(finish_content=finishContent, edit_content=editContent)
			part.edited_page=int(request.POST['page'])
			part.save()
			status = 'success'
			message = u'您上次儲存時間為：{0}，請定時存檔喔~'.format(timezone.now())
		elif request.POST.has_key('close'):
			status = 'success'
			message = u'關閉無儲存資料'
			redirect_to = reverse('account:service')
		elif request.POST.has_key('finish'):
			part.set_content(finish_content=content, edit_content='')
			part.change_status(1, 'review')
			status = 'success'
			message = u'完成文件校對，將進入審核'
			redirect_to = reverse('account:service')
			event = Event.objects.create(creater=request.user, action=part)
		elif request.POST.has_key('load'):
			part.load_full_content()
			status = 'success'
			message = u'成功載入全部文件內容'
		[scanPageList, defaultPageURL] = part.get_image(request.user)
		editContent = part.get_content('-edit')
		del request.session['postToken']
		postToken = uuid.uuid1().hex
		request.session['postToken'] = postToken
		print request.session.get('postToken',default=None)
		return locals()
	if request.method == 'GET':
		postToken = uuid.uuid1().hex
		request.session['postToken'] = postToken
		return locals()

@user_category_check('advanced_editor')
@http_response
def full_edit(request, ISBN_part, template_name='ebookSystem/full_edit.html'):
	try:
		part = EBook.objects.get(ISBN_part=ISBN_part)
	except:
		raise Http404("book does not exist")
	[scanPageList, defaultPageURL] = part.get_image(request.user)
	editContent = part.get_content('-sc')
	if request.method == 'POST':
		with codecs.open(part.get_path('-sc'), 'w', encoding='utf-8') as scFile:
			scFile.write(u'\ufeff' +request.POST['content'])
		return locals()
	if request.method == 'GET':
		return locals()

@user_category_check('advanced_editor')
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
			status = u'success'
			message = u'重新檢查特殊內容成功'
		if request.POST.has_key('full_write'):
			for sc in part.specialcontent_set.all():
				sc.write_to_file()
			status = u'success'
			message = u'全寫入成功'
		if request.POST.has_key('finish'):
			if part.is_sc_rebuild:
				status = u'error'
				message = u'請先進行特殊內容檢查'
				return locals()
			if not len(part.specialcontent_set.all()) == 0:
				status = u'error'
				message = u'請先完成特殊內容編輯'
				return locals()
			part.change_status(1, 'sc_finish')
			status = u'success'
			message = u'特殊內容編輯完成'
			redirect_to = reverse('account:sc_service')
		if request.POST.has_key('write'):
			sc = SpecialContent.objects.get(id=request.POST['write'])
			sc.write_to_file()
			status = u'success'
			message = u'寫入動作成功'
		return locals()
	if request.method == 'GET':
		return locals()

@user_category_check('advanced_editor')
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
	elif page == part.end_page -part.begin_page:
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
		image_path = sc.ebook.book.path +'/OCR/resource/image_' +sc.id +'.jpg'
		image_public_path = sc.ebook.get_path('public') +'/OCR/resource/image_' +sc.id +'.jpg'
		preview_image_url = image_public_path.replace(BASE_DIR +'/static/', '')
		editContent = img_tag['alt']
	elif type == 'unknown':
		editContent = sc.content
	template_name = 'ebookSystem/edit_{0}.html'.format(type)
	if request.method == 'POST':
		if request.POST.has_key('save') or request.POST.has_key('write'):
			if type == 'image':
				img_tag['src'] = 'resource/' +sc.id +'.jpg'
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