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
			return HttpResponseRedirect(redirect_to)
	if request.method == 'GET':
		registerUserForm = RegisterUserForm()
		return render(request, template_name, locals())

def login_user(request, template_name='registration/login.html'):
	error_message='';
	if request.method == 'GET':
		loginForm = LoginForm()
	if request.method == 'POST':
		loginForm = LoginForm(request.POST)
		if loginForm.is_valid():
			username = loginForm.cleaned_data['username']
			password = loginForm.cleaned_data['password']
			user = authenticate(username=username, password=password)
			if user is not None:
				if user.is_active:
					login(request, user)
					redirect_to = redirect_user(user)
					if request.is_ajax():
						resp={};
						resp['status']='success';
						resp['message']=redirect_to;
						return HttpResponse(json.dumps(resp), content_type="application/json");
					else:
						return HttpResponseRedirect(redirect_to); 
				else:
					error_message = u'您的帳號非啟用'
			else:
				error_message = u'您的帳號或密碼錯誤'
	if request.is_ajax():
		resp={};
		resp['status']='error';
		resp['message']=error_message;
		return HttpResponse(json.dumps(resp), content_type="application/json");
	return render(request, template_name, locals())

def logout_user(request, template_name='registration/logged_out.html'):
	logout(request)
	return render(request, template_name, locals())

def redirect_user(user):
	if user.is_editor():
		return reverse('account:profile')
	if user.is_guest():
		return reverse('guest:create_document')