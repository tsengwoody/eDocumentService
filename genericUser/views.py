# coding: utf-8
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse
from django.http import HttpResponse,HttpResponseRedirect
from django.utils import timezone
from django.shortcuts import render, get_list_or_404

from account.models import Editor
from ebookSystem.models import *
from guest.models import Guest
from genericUser.models import *
from utils.decorator import *
from utils.uploadFile import handle_uploaded_file
from utils.zip import *
from .forms import *
from mysite.settings import PREFIX_PATH,INACTIVE, ACTIVE, EDIT, REVIEW, REVISE, FINISH, MANAGER, SERVICE
from zipfile import ZipFile
import json
import shutil


@user_category_check(['scaner'])
@http_response
def create_document(request, template_name='genericUser/create_document.html'):
	readme_url = request.path +'readme/'
	user = request.user
	if request.method == 'POST':
		bookForm = BookForm(request.POST, request.FILES)
		if not bookForm.is_valid():
			status = 'error'
			message = u'表單驗證失敗' +str(bookForm.errors)
			return locals()
		uploadPath = PREFIX_PATH +u'static/ebookSystem/document/{0}'.format(bookForm.cleaned_data['ISBN'])
		if os.path.exists(uploadPath):
			status = 'error'
			message = u'文件已存在'
			return locals()
		[status, message] = handle_uploaded_file(uploadPath, request.FILES['fileObject'])
		uploadFilePath = os.path.join(uploadPath, request.FILES['fileObject'].name)
		try:
			with ZipFile(uploadFilePath, 'r') as uploadFile:
				ZipFile.testzip(uploadFile)
		except:
				shutil.rmtree(uploadPath)
				status = 'error'
				message = u'非正確ZIP文件'
				return locals()
		unzip_file(uploadFilePath, uploadPath)
		newBook = bookForm.save(commit=False)
		newBook.path = uploadPath
		if not newBook.validate_folder():
			shutil.rmtree(uploadPath)
			status = 'error'
			message = u'上傳壓縮文件結構錯誤，詳細結構請參考說明頁面'
			return locals()
		newBook.scaner = user
		newBook.save()
		newBook.create_EBook()
		if request.POST.has_key('guest'):
			try:
				guest = Guest.objects.get(user__username=request.POST['guest'])
				newBook.guests.add(guest)
			except:
				guest = None
		else:
			guest = None
		event = Event.objects.create(creater=user, action=newBook)
		redirect_to = reverse('guest:profile')
		status = 'success'
		message = u'成功建立並上傳文件'
		return locals()
	if request.method == 'GET':
		bookForm = BookForm()
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

@user_category_check(['manager'])
def review_user(request, username, template_name='genericUser/review_user.html'):
	user = get_list_or_404(User, username=username)[0]
	sourcePath = PREFIX_PATH +'static/ebookSystem/disability_card/{0}'.format(user.username)
	frontPage = user.username +'_front.jpg'
	frontPageURL = sourcePath +u'/' +frontPage
	frontPageURL = frontPageURL.replace(PREFIX_PATH +'static/', '')
	backPage = user.username +'_back.jpg'
	backPageURL = sourcePath +u'/' +backPage
	backPageURL = backPageURL.replace(PREFIX_PATH +'static/', '')
	if request.method == 'GET':
		return render(request, template_name, locals())
	if request.method == 'POST':
		response = {}
		redirect_to = None
		if request.POST.has_key('active_login'):
			user.is_active = True
			response['status'] = 'success'
			response['message'] = u'已啟用登錄權限'
		elif request.POST.has_key('active_editor'):
			user.is_editor = True
			response['status'] = 'success'
			response['message'] = u'已啟用editor權限'
		elif request.POST.has_key('active_guest') :
			user.is_guest = True
			response['status'] = 'success'
			response['message'] = u'已啟用guest權限'
		elif request.POST.has_key('active_scaner'):
			user.is_scaner = True
			response['status'] = 'success'
			response['message'] = u'已啟用scaner權限'
		elif request.POST.has_key('inactive_login'):
			print 'inactive_login'
			user.is_active = False
			response['status'] = 'success'
			response['message'] = u'停用用登錄權限'
		elif request.POST.has_key('inactive_editor'):
			user.is_editor = False
			response['status'] = 'success'
			response['message'] = u'已停用editor權限'
		elif request.POST.has_key('inactive_guest'):
			user.is_guest = False
			response['status'] = 'success'
			response['message'] = u'已停用guest權限'
		elif request.POST.has_key('inactive_scaner'):
			user.is_scaner = False
			response['status'] = 'success'
			response['message'] = u'已停用scaner權限'
		elif request.POST.has_key('finish'):
			user.status = ACTIVE
			redirect_to = reverse('manager:review_user_list')
			response['status'] = 'success'
			response['message'] = u'完成審核權限開通'
		elif request.POST.has_key('error'):
			user.status = REVISE
			redirect_to = reverse('manager:review_user_list')
			response['status'] = 'success'
			response['message'] = u'資料異常退回'
		user.save()
		status = response['status']
		message = response['message']
		if request.is_ajax():
			return HttpResponse(json.dumps(response), content_type="application/json")
		else:
			if redirect_to:
				return HttpResponseRedirect(redirect_to)
			else:
				return render(request, template_name, locals())

@user_category_check(['user'])
def info(request, template_name):
	user = request.user
	return render(request, template_name, locals())

@user_category_check(['user'])
def info_change(request,template_name):
	user = request.user
	if request.method == 'POST':
		infoChangeUserForm = InfoChangeUserForm(request.POST, instance = user)
		if infoChangeUserForm.is_valid():
			infoChangeUserForm.save()
			user.status = REVIEW
			user.save()
			redirect_to = reverse('genericUser:info')
			return HttpResponseRedirect(redirect_to)
	if request.method == 'GET':
		infoChangeUserForm = InfoChangeUserForm(instance = user)
	return render(request, template_name, locals())

@user_category_check(['user'])
@http_response
def revise_content(request, template_name='genericUser/revise_content.html'):
	user = request.user
	if request.method == 'GET':
		return locals()
	if request.method == 'POST':
		if not (request.POST.has_key('book_ISBN') and request.POST.has_key('part') and request.POST.has_key('content')):
			status = 'error'
			message = u'表單填寫錯誤'
			return locals()
		book_ISBN = request.POST['book_ISBN']
		part = request.POST['part']
		content = request.POST['content']
		book = Book.objects.get(ISBN=book_ISBN)
		ebook = EBook.objects.get(part=part, book=book)
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
	user = request.user
	if request.method == 'POST':
		if request.POST.has_key('editor'):
			if user.has_editor():
				service_hours=int(request.POST['service_hours'])
				newEditor = Editor(user=user, professional_field=request.POST['professional_field'], service_hours=service_hours)
			else:
				newEditor = Editor(user=user, professional_field=request.POST['professional_field'])
			newEditor.save()
			user.status = REVIEW
			user.save()
			status = 'success'
			message = u'editor申請成功'
		if request.POST.has_key('guest'):
			uploadDir = PREFIX_PATH +'static/ebookSystem/disability_card/{0}'.format(user.username)
			if os.path.exists(uploadDir):
				shutil.rmtree(uploadDir)
			request.FILES['disability_card_front'].name = user.username +'_front.jpg'
			[status, message] = handle_uploaded_file(uploadDir, request.FILES['disability_card_front'])
			request.FILES['disability_card_back'].name = user.username +'_back.jpg'
			[status, message] = handle_uploaded_file(uploadDir, request.FILES['disability_card_back'])
			if not user.has_guest():
				newGuest = Guest(user=user)
				newGuest.save()
				user.status = REVIEW
				user.save()
				status = 'success'
				message = u'guest申請成功'
			else:
				user.status = REVIEW
				user.save()
				status = 'success'
				message = u'guest申請成功'
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

from django.contrib import messages
def test_message(request, template_name):
	messages.add_message(request, messages.INFO, 'Hello world.')
	messages.add_message(request, messages.INFO, 'Hello world2.')
	storage = messages.get_messages(request)
	for message in storage:
		print message.tags
	return render(request, template_name, locals())