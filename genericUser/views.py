# coding: utf-8
from django.core.cache import cache
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render, get_list_or_404
from django.utils import timezone
from account.models import Editor
from ebookSystem.models import *
from guest.models import Guest
from genericUser.models import *
from utils.decorator import *
from utils.uploadFile import handle_uploaded_file
from utils.zip import *
from .forms import *
from mysite.settings import BASE_DIR,SERVICE,OTP_ACCOUNT,OTP_PASSWORD
from zipfile import ZipFile
import json
import shutil
import datetime
import requests
import urllib,urllib2

@user_category_check(['guest'])
@http_response
def create_document(request, template_name='genericUser/create_document.html'):
	readme_url = request.path +'readme/'
	if request.method == 'POST':
		bookInfoForm = BookInfoForm(request.POST)
		if not bookInfoForm.is_valid() and not bookInfoForm.errors.has_key('ISBN'):
			status = 'error'
			message = u'表單驗證失敗' +str(bookInfoForm.errors)
			return locals()
		uploadPath = BASE_DIR +u'/file/ebookSystem/document/{0}'.format(request.POST['ISBN'])
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
		try:
			newBookInfo = BookInfo.objects.get(ISBN=request.POST['ISBN'])
		except:
			newBookInfo = bookInfoForm.save()
		newBook = Book(book_info=newBookInfo, ISBN=request.POST['ISBN'])
		newBook.path = uploadPath
		if not newBook.validate_folder():
			shutil.rmtree(uploadPath)
			status = 'error'
			message = u'上傳壓縮文件結構錯誤，詳細結構請參考說明頁面'
			return locals()
		newBook.scaner = request.user
		newBook.owner = request.user
		if request.POST.has_key('designate'):
			newBook.is_private = True
		newBook.save()
		newBook.create_EBook()
		event = Event.objects.create(creater=request.user, action=newBook)
		redirect_to = '/'
		status = 'success'
		message = u'成功建立並上傳文件'
		return locals()
	if request.method == 'GET':
		return locals()

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
		cache_key = "%s_%s" % (request.META['REMOTE_ADDR'], progress_id)
		data = cache.get(cache_key)
#		cache_key = "%s" % (progress_id)
#		data = request.session.get('upload_progress_%s' % cache_key, None)
		return HttpResponse(json.dumps(data), content_type="application/json")
	else:
		return HttpResponseServerError('Server Error: You must provide X-Progress-ID header or query param.')

@http_response
def apply_document(request, template_name='genericUser/apply_document.html'):
	user = request.user
	if request.method == 'POST':
		bookInfoForm = BookInfoForm(request.POST)
		if not bookInfoForm.is_valid():
			status = 'error'
			message = u'表單驗證失敗' +str(bookInfoForm.errors)
			return locals()
		newBookInfo = bookInfoForm.save()
		applyDocumentAction = ApplyDocumentAction.objects.create(book_info=newBookInfo)
		event = Event.objects.create(creater=user, action=applyDocumentAction)
		redirect_to = '/'
		status = 'success'
		message = u'成功申請代掃描辨識，請將書籍寄至所選之中心'
		return locals()
	if request.method == 'GET':
		return locals()

@user_category_check(['user'])
def event_list(request):
	events = Event.objects.filter(creater=request.user)
	template_name = 'genericUser/event_list.html'
	return render(request, template_name, locals())


def func_desc(request, template_name='genericUser/func_desc.html'):
	return render(request, template_name, locals())

def license(request, template_name='genericUser/license.html'):
	return render(request, template_name, locals())

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

@http_response
def review_user(request, username, template_name='genericUser/review_user.html'):
	try:
		user = User.objects.get(username=username)
	except:
		raise Http404("user does not exist")
	events = Event.objects.filter(content_type__model='user', object_id=user.id, status=Event.STATUS['review'])
	sourcePath = BASE_DIR +'/static/ebookSystem/disability_card/{0}'.format(user.username)
	frontPage = user.username +'_front.jpg'
	frontPageURL = sourcePath +u'/' +frontPage
	frontPageURL = frontPageURL.replace(BASE_DIR +'/static/', '')
	backPage = user.username +'_back.jpg'
	backPageURL = sourcePath +u'/' +backPage
	backPageURL = backPageURL.replace(BASE_DIR +'/static/', '')
	if request.method == 'GET':
		return locals()
	if request.method == 'POST':
		if request.POST.has_key('login'):
			user.is_active = True
		else:
			user.is_active = False
		if request.POST.has_key('editor'):
			user.is_editor = True
			status = 'success'
			message = u'已啟用editor權限'
		else:
			user.is_editor = False
			status = 'success'
			message = u'已停用editor權限'
		if request.POST.has_key('guest') :
			user.is_guest = True
			status = 'success'
			message = u'已啟用guest權限'
		else:
			user.is_guest = False
			status = 'success'
			message = u'已停用guest權限'
		if request.POST['review'] == 'success':
			user.status = user.STATUS['active']
			redirect_to = reverse('manager:event_list', kwargs={'action':'user' })
			status = 'success'
			message = u'完成審核權限開通'
			for event in events:
				event.response(status=status, message=message, user=request.user)
			user.save()
		elif request.POST['review'] == 'error':
			redirect_to = reverse('manager:event_list', kwargs={'action':'user' })
			status = 'success'
			message = u'資料異常退回'
			for event in events:
				event.response(status='error', message=request.POST['reason'], user=request.user)
		return locals()

@user_category_check(['user'])
@http_response
def info(request, template_name):
	user = request.user
	if request.method == 'POST':
		if request.POST.has_key('email') and (not request.user.email == request.POST['email']):
			request.user.email = request.POST['email']
			request.user.auth_email = False
			request.user.save()
			status = u'success'
			message = u'修改資料成功，請重新驗證。'
		if request.POST.has_key('phone') and (not request.user.phone == request.POST['phone']):
			request.user.phone = request.POST['phone']
			request.user.auth_phone = False
			request.user.save()
			status = u'success'
			message = u'修改資料成功，請重新驗證。'
		status = u'success'
		message = u'無資料修改。'
		return locals()
	if request.method == 'GET':
		return locals()

@user_category_check(['user'])
@http_response
def change_contact_info(request, template_name):
	if request.method == 'POST':
		if request.POST.has_key('email') and (not request.user.email == request.POST['email']):
			request.user.email = request.POST['email']
			request.user.auth_email = False
			request.user.save()
			status = u'success'
			message = u'修改資料成功，請重新驗證。'
		if request.POST.has_key('phone') and (not request.user.phone == request.POST['phone']):
			request.user.phone = request.POST['phone']
			request.user.auth_phone = False
			request.user.save()
			status = u'success'
			message = u'修改資料成功，請重新驗證。'
		status = u'success'
		message = u'無資料修改。'
		redirect_to = reverse('genericUser:info')
		return locals()
	if request.method == 'GET':
		return locals()

@user_category_check(['user'])
@http_response
def revise_content(request, template_name='genericUser/revise_content.html'):
	user = request.user
	if request.method == 'GET':
		return locals()
	if request.method == 'POST':
		if not (request.POST['book_ISBN']!='' and request.POST['content']!='' and request.POST['part']!=''):
			status = 'error'
			message = u'表單填寫錯誤'
			return locals()
		book_ISBN = request.POST['book_ISBN']
		part = request.POST['part']
		content = request.POST['content']
		ISBN_part = request.POST['book_ISBN'] +'-' +request.POST['part']
		ebook = EBook.objects.get(ISBN_part=ISBN_part)
		result = ebook.fuzzy_string_search(string = content, length=10, action='-final')
		if len(result) == 1:
			status = 'success'
			message = u'成功搜尋到修政文字段落'
			reviseContentAction = ReviseContentAction.objects.create(ebook=ebook, content=content)
			event = Event.objects.create(creater=user, action=reviseContentAction)
		elif len(result) == 0:
			status = 'error'
			message = u'搜尋不到修政文字段落，請重新輸入並多傳送些文字'
		else:
			status = 'error'
			message = u'搜尋到多處修政文字段落，請重新輸入並多傳送些文字'
		return locals()

@http_response
def set_role(request,template_name='genericUser/set_role.html'):
	if request.method == 'POST':
		if request.user.has_editor():
			request.user.editor.professional_field = request.POST['professional_field']
		if request.user.has_guest():
			uploadDir = BASE_DIR +'/static/ebookSystem/disability_card/{0}'.format(user.username)
			if os.path.exists(uploadDir):
				shutil.rmtree(uploadDir)
			request.FILES['disability_card_front'].name = user.username +'_front.jpg'
			handle_uploaded_file(uploadDir, request.FILES['disability_card_front'])[0]
			request.FILES['disability_card_back'].name = user.username +'_back.jpg'
			handle_uploaded_file(uploadDir, request.FILES['disability_card_back'])[0]
		status = u'success'
		message = u'角色設定成功'
		return locals()
	if request.method == 'GET':
		return locals()

@http_response
def contact_us(request, template_name='genericUser/contact_us.html'):
	if request.method == 'GET':
		contactUsForm = ContactUsForm()
		return locals()
	if request.method == 'POST':
		contactUsForm = ContactUsForm(request.POST)
		if not contactUsForm.is_valid():
			status = 'error'
			message = u'表單驗證失敗{}'.format(contactUsForm.errors)
			return locals()
		contactUs = contactUsForm.save(commit=False)
		contactUs.message_datetime = timezone.now()
		subject = u'[{}] {}'.format (contactUs.kind, contactUs.subject)
		body = u'姓名:'+ contactUs.name+ u'\nemail:'+ contactUs.email+ u'\n內容：\n'+ contactUs.content
		email = EmailMessage(subject=subject, body=body, from_email=SERVICE, to=MANAGER)
		email.send(fail_silently=False)
		contactUs.save()
		if request.user.is_authenticated():redirect_to = reverse('account:profile')
		status = 'success'
		message = u'成功寄送內容，我們將盡速回復'
		return locals()

@user_category_check(['user'])
@http_response
def servicehours_list(request, template_name='genericUser/servicehours_list.html'):
	month_day = datetime.date(year=datetime.date.today().year, month=datetime.date.today().month, day=1)
	try:
		current_ServiceHours = ServiceHours.objects.get(date=month_day, user=request.user)
	except:
		pass
	ServiceHours_list = ServiceHours.objects.filter(user=request.user).exclude(date=month_day)
	if request.method == 'POST':
		if request.POST.has_key('exchange'):
			exchange_serviceHours = ServiceHours.objects.get(id=request.POST['exchange'])
			exchange_serviceHours.is_exchange=True
			exchange_serviceHours.save()
		return locals()
	if request.method == 'GET':
		return locals()

@http_response
def verify_contact_info(request, template='genericUser/verify_contact_info.html'):
	if not request.is_ajax():
		status = u'error'
		message = u'非ajax請求'
	if request.POST.has_key('generate'):
		if request.POST['generate'] == 'email':
			if not cache.has_key(request.user.email):
				import random
				import string
				vcode = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
				cache.set(request.user.email, {'vcode':vcode}, 600)
			else:
				vcode = cache.get(request.user.email)['vcode']
			from django.core.mail import EmailMessage
			subject = u'[驗證] {0} 信箱驗證碼'.format(request.user.username)
			body = u'親愛的{0}您的信箱驗證碼為：{1}，請在10分鐘內輸入。\n'.format(request.user.username, vcode)
			email = EmailMessage(subject=subject, body=body, from_email=SERVICE, to=[request.user.email])
			email.send(fail_silently=False)
			status = 'success'
			message = u'已寄送到您的電子信箱'
		elif request.POST['generate'] == 'phone':
			if not cache.has_key(request.user.phone):
				import random
				import string
				vcode = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
				cache.set(request.user.phone, {'vcode':vcode}, 600)
			else:
				vcode = cache.get(request.user.phone)['vcode']
			data= u'親愛的{0}您的信箱驗證碼為：{1}，請在10分鐘內輸入。\n'.format(request.user.username, vcode)
			url = 'https://api.kotsms.com.tw/kotsmsapi-1.php?username={0}&password={1}&dstaddr={2}&smbody={3}'.format(OTP_ACCOUNT, OTP_PASSWORD, request.user.phone, urllib.quote(data.encode('big5')))
			session = requests.Session()
			response = session.get(url)
			print(response.text.split('=')[1])
			if response.text.split('=')[1] > 0:
				status = 'success'
				message = u'已寄送到您的手機'
			else:
				status = 'error'
				message = u'請確認手機號碼是否正確或聯絡系統管理員'
		return locals()
	if request.POST.has_key('verification_code') and request.POST.has_key('type'):
		if request.POST['type'] == 'email':
			if not cache.has_key(request.user.email):
				status = u'error'
				message = u'驗證碼已過期，請重新產生驗證碼'
				return locals()
			input_vcode = request.POST['verification_code']
			vcode = cache.get(request.user.email)['vcode']
			if input_vcode == vcode:
				status = u'success'
				message = u'信箱驗證通過'
				request.user.auth_email=True
				request.user.save()
			else:
				status = u'error'
				message = u'信箱驗證碼不符'
		if request.POST['type'] == 'phone':
			if not cache.has_key(request.user.phone):
				status = u'error'
				message = u'驗證碼已過期，請重新產生驗證碼'
				return locals()
			input_vcode = request.POST['verification_code']
			vcode = cache.get(request.user.phone)['vcode']
			if input_vcode == vcode:
				status = u'success'
				message = u'手機驗證通過'
				request.user.auth_phone=True
				request.user.save()
			else:
				status = u'error'
				message = u'手機驗證碼不符'
		return locals()

from django.contrib import messages
def test_message(request, template_name):
	messages.add_message(request, messages.INFO, 'Hello world.')
	messages.add_message(request, messages.INFO, 'Hello world2.')
	storage = messages.get_messages(request)
	for message in storage:
		print message.tags
	return render(request, template_name, locals())