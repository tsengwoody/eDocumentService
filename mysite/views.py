# coding: utf-8
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render
from .forms import *
from ebookSystem.models import *
from utils.uploadFile import *
from utils.decorator import *
from mysite.settings import PREFIX_PATH
import json

def home(request, template_name='home.html'):
	return render(request, template_name, locals())

@http_response
def register(request, template_name='registration/register.html'):
	if request.method == 'POST':
		registerUserForm = RegisterUserForm(request.POST)
		if not registerUserForm.is_valid():
			status = 'error'
			message = u'表單驗證失敗' +str(registerUserForm.errors)
			return locals()
		newUser = registerUserForm.save(commit=False)
		newUser.set_password(request.POST.get('password'))
		newUser.is_active = True
		newUser.save()
		redirect_to = reverse('login')
		status = 'success'
		message = u'註冊成功，請等待帳號審核'
		if request.POST.has_key('editor'):
			try:
				newEditor = Editor(user=newUser, service_hours=0, professional_field=request.POST['professional_field'])
				newEditor.save()
			except:
				status = 'error'
				message = u'editor申請失敗'
		if request.POST.has_key('guest'):
			try:
				request.FILES['disability_card_front']
				request.FILES['disability_card_back']
			except:
				status = 'error'
				message = u'無上傳文件'
				return locals()
			uploadDir = PREFIX_PATH +'static/ebookSystem/disability_card/{0}'.format(newUser.username)
			request.FILES['disability_card_front'].name = request.POST['username'] +'_front.jpg'
			[status, message] = handle_uploaded_file(uploadDir, request.FILES['disability_card_front'])
			request.FILES['disability_card_back'].name = request.POST['username'] +'_back.jpg'
			[status, message] = handle_uploaded_file(uploadDir, request.FILES['disability_card_back'])
			try:
				newGuest = Guest(user=newUser)
				newGuest.save()
			except:
				status = 'error'
				message = u'guest申請失敗'
		return locals()
	if request.method == 'GET':
		registerUserForm = RegisterUserForm()
		return locals()

from utils.decorator import *
#@audio_code_valid
@http_response
def login_user(request, template_name='registration/login.html', *args, **kwargs):
	try:
		UUID = locals()['kwargs']['UUID']
		code = cache.get(UUID)
	except:
		pass
	if request.method == 'GET':
		loginForm = LoginForm()
		return locals()
	if request.method == 'POST':
		loginForm = LoginForm(request.POST)
		if not loginForm.is_valid():
			status = 'error'
			message = u'表單驗證失敗'
			return locals()
		username = loginForm.cleaned_data['username']
		password = loginForm.cleaned_data['password']
		user = authenticate(username=username, password=password)
		if user is None:
			status = 'error'
			message = u'您的帳號或密碼錯誤'
			return locals()
		if not user.is_active:
			status = 'error'
			message = u'您的帳號尚未啟用，管理員審核中，若超過3日未啟用或未收到管理員身份認證，請利用聯絡我們進行反應'
			return locals()
		from django.contrib.sessions.models import Session
		for session in Session.objects.all():
			if session.get_decoded().has_key('_auth_user_id') and int(session.get_decoded()['_auth_user_id']) == user.id:
				session.delete()
		login(request, user)
		redirect_to = redirect_user(user)
		status = 'success'
		message = u'登錄成功'
		return locals()

def logout_user(request, template_name='registration/logged_out.html'):
	logout(request)
	return render(request, template_name, locals())

def redirect_user(user):
	if user.is_editor and user.has_editor():
		return reverse('account:profile')
	if user.is_guest and user.has_guest():
		return reverse('guest:profile')
	return reverse('genericUser:info')

import locale
import sys

def view_locale(request):
	loc_info = "getlocale: " + str(locale.getlocale()) + \
		"<br/>getdefaultlocale(): " + str(locale.getdefaultlocale()) + \
		"<br/>fs_encoding: " + str(sys.getfilesystemencoding()) + \
		"<br/>sys default encoding: " + str(sys.getdefaultencoding())
	return HttpResponse(loc_info)