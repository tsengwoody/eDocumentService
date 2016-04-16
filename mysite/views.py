# coding: utf-8
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render
from .forms import *
from ebookSystem.models import *
import json

def register(request, template_name='registration/register.html'):
	if request.method == 'POST':
		response = {}
		redirect_to = None
		registerUserForm = RegisterUserForm(request.POST)
		if registerUserForm.is_valid():
			newUser = registerUserForm.save(commit=False)
			newUser.set_password(request.POST.get('password'))
			newUser.is_active = True
			newUser.save()
			if request.POST['role'] == 'Editor':
				newEditor = Editor(user=newUser, service_hours=0)
				newEditor.save()
			elif request.POST['role'] == 'Guest':
				newGuest = Guest(user=newUser)
				newGuest.save()
			redirect_to = reverse('login')
			response['status'] = 'success'
			response['message'] = u'註冊成功，請等待帳號審核'
			response['redirect_to'] = redirect_to
		else :
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
	if request.method == 'GET':
		registerUserForm = RegisterUserForm()
		return render(request, template_name, locals())

def login_user(request, template_name='registration/login.html'):
	if request.method == 'GET':
		loginForm = LoginForm()
		return render(request, template_name, locals())
	if request.method == 'POST':
		response = {}
		redirect_to = None
		loginForm = LoginForm(request.POST)
		if loginForm.is_valid():
			username = loginForm.cleaned_data['username']
			password = loginForm.cleaned_data['password']
			user = authenticate(username=username, password=password)
			if user is not None:
#				if user.is_active:
				login(request, user)
				redirect_to = redirect_user(user)
				response['status'] = 'success'
				response['message'] = u'登錄成功'
				response['redirect_to'] = redirect_to
#				else:
#					response['status'] = 'error'
#					response['message'] = u'您的帳號尚未啟用，管理員審核中，若超過3日未啟用或未收到管理員身份認證，請利用聯絡我們進行反應'
			else:
				response['status'] = 'error'
				response['message'] = u'您的帳號或密碼錯誤'
		else :
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

def logout_user(request, template_name='registration/logged_out.html'):
	logout(request)
	return render(request, template_name, locals())

def redirect_user(user):
	if user.is_editor():
		return reverse('account:profile')
	if user.is_guest():
		return reverse('guest:create_document')