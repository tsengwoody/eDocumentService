# coding: utf-8
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse
from django.http import HttpResponse,HttpResponseRedirect
from django.utils import timezone
from django.shortcuts import render, get_list_or_404
import json

from account.models import Editor
from ebookSystem.models import *
from guest.models import Guest
from genericUser.models import User
from utils.decorator import *
from utils.uploadFile import handle_uploaded_file
from mysite.settings import PREFIX_PATH,INACTIVE, ACTIVE, EDIT, REVIEW, REVISE, FINISH
from .forms import *

MANAGER = ['tsengwoody@yahoo.com.tw']
SERVICE = 'tsengwoody.tw@gmail.com'

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

@user_category_check(['editor', 'guest'])
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

def set_role(request,template_name='genericUser/set_role.html'):
	user = request.user
	if request.method == 'POST':
		response = {}
		if request.POST.has_key('editor'):
			newEditor = Editor(user=user, professional_field=request.POST['professional_field'], service_hours=request.POST['service_hours'])
			newEditor.save()
			user.status = REVIEW
			user.save()
			response['status'] = 'success'
			response['message'] = u'editor申請成功'
		if request.POST.has_key('guest'):
			uploadDir = PREFIX_PATH +'static/ebookSystem/disability_card/{0}'.format(user.username)
			request.FILES['disability_card_front'].name = user.username +'_front.jpg'
			response = handle_uploaded_file(uploadDir, request.FILES['disability_card_front'])
			request.FILES['disability_card_back'].name = user.username +'_back.jpg'
			response = handle_uploaded_file(uploadDir, request.FILES['disability_card_back'])
			if not user.has_guest():
				newGuest = Guest(user=user)
				newGuest.save()
				user.status = REVIEW
				user.save()
				response['status'] = 'success'
				response['message'] = u'guest申請成功'
			else:
				response['status'] = 'error'
				response['message'] = u'guest申請失敗，已有此權限'
		status = response['status']
		message = response['message']
		if request.is_ajax():
			return HttpResponse(json.dumps(response), content_type="application/json")
		else:
			return render(request, template_name, locals())
	if request.method == 'GET':
		return render(request, template_name, locals())

def contact_us(request, template_name='genericUser/contact_us.html'):
	if request.method == 'GET':
		contactUsForm = ContactUsForm()
		return render(request, template_name, locals())
	if request.method == 'POST':
		response = {}
		redirect_to = None
		contactUsForm = ContactUsForm(request.POST)
		if contactUsForm.is_valid():
			contactUs = contactUsForm.save(commit=False)
			contactUs.message_datetime = timezone.now()
			subject = u'[{}] {}'.format (contactUs.kind, contactUs.subject)
			body = u'姓名:'+ contactUs.name+ u'\nemail:'+ contactUs.email+ u'\n內容：\n'+ contactUs.content
			email = EmailMessage(subject=subject, body=body, from_email=SERVICE, to=MANAGER)
			email.send(fail_silently=False)
			contactUs.save()
			redirect_to = reverse('account:profile')
			response['status'] = 'success'
			response['message'] = u'成功寄送內容，我們將盡速回復'
		else:
			response['status'] = 'error'
			response['message'] = u'表單驗證失敗'
		status = response['status']
		message = response['message']
		if request.is_ajax():
			return HttpResponse(json.dumps(response), content_type="application/json")
		else:
#			if redirect_to:
#				return HttpResponseRedirect(redirect_to)
#			else:
			return render(request, template_name, locals())

def readme(request, template_name):
	template_name = 'account/' +template_name +'_readme.html'
	return render(request, template_name, locals())