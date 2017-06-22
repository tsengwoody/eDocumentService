# coding: utf-8
from django.contrib.auth import (login as auth_login, logout as auth_logout, update_session_auth_hash, authenticate,)
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.core.urlresolvers import reverse, resolve
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render
from .forms import *
from ebookSystem.models import *
from genericUser.models import *
from utils.uploadFile import *
from utils.decorator import *
from mysite.settings import BASE_DIR
import json

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


@http_response
def home(request, template_name='home.html'):
#	logger.info('{}/home\t{}'.format(resolve(request.path).namespace, request.user))
	article_list = Article.objects.all().order_by('-datetime')
	return locals()

@http_response
def register(request, template_name='registration/register.html'):
	if request.method == 'POST':
#		print request.POST
		registerUserForm = RegisterUserForm(request.POST)
		if not registerUserForm.is_valid():
			status = 'error'
			message = u'表單驗證失敗' +str(registerUserForm.errors)
			return locals()
		if 'is_privacy' not in request.POST:
			status = 'error'
			message = u'請勾選隱私權條款'
			return locals()
		newUser = registerUserForm.save(commit=False)
		newUser.set_password(request.POST.get('password'))
		newUser.is_active = True
		newUser.is_license = True
		newUser.save()
		newUser.permission.add(
			Permission.objects.get(codename='active'),
			Permission.objects.get(codename='license'),
		)
		if request.POST['role'] == 'Editor':
			try:
				newEditor = Editor.objects.create(user=newUser, professional_field=request.POST['professional_field'])
				newUser.is_editor = True
				newUser.permission.add(Permission.objects.get(codename='editor'))
			except:
				newUser.delete()
				status = 'error'
				message = u'editor申請失敗'
				return locals()
		elif request.POST['role'] == 'Guest':
			try:
				DCDir = BASE_DIR +'/static/ebookSystem/disability_card/{0}'.format(newUser.username)
				[status, message] = handle_uploaded_file(os.path.join(DCDir, request.POST['username'] + '_front.jpg'), request.FILES['disability_card_front'])
				[status, message] = handle_uploaded_file(os.path.join(DCDir, request.POST['username'] + '_back.jpg'), request.FILES['disability_card_back'])
				newGuest = Guest.objects.create(user=newUser)
			except:
				newUser.delete()
				status = 'error'
				message = u'guest申請失敗'
				return locals()
		newUser.save()
		Event.objects.create(creater=newUser, action=newUser)
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			auth_login(request, user)
		else:
			pass
		status = 'success'
		message = u'註冊成功，請進行通訊資料驗證'
		redirect_to = reverse('genericUser:info')
		return locals()
	if request.method == 'GET':
		registerUserForm = RegisterUserForm()
		return locals()

from utils.decorator import *
@http_response
def login(request, template_name='registration/login.html', authentication_form=AuthenticationForm):
	"""
	Displays the login form and handles the login action.
	"""
	try:
		UUID = locals()['kwargs']['UUID']
		code = cache.get(UUID)
	except:
		pass
	if request.method == 'GET':
		form = authentication_form(request)
		captcha=FormWithCaptcha();
		return locals()
	if request.method == 'POST':
		form = authentication_form(request, data=request.POST)
		reCaptcha = FormWithCaptcha(request.POST);
#		if not reCaptcha.is_valid():
#			status = 'error'
#			message = u'captcha驗證失敗，'+ str(reCaptcha.errors)
#			return locals()
		if not form.is_valid():
			status = 'error'
			message = u'表單驗證失敗，' + str(form.errors)
			return locals()

		auth_login(request, form.get_user())
		if Permission.objects.get(codename='license') not in request.user.permission.all():
			redirect_to='/genericUser/license/'
		else:
			redirect_to = '/'
		from django.contrib.sessions.models import Session
		for session in Session.objects.all():
			try:
				if int(session.get_decoded()['_auth_user_id']) == request.user.id and request.user.username != 'root':
					session.delete()
			except:
				pass
		status = 'success'
		message = u'登錄成功'
		return locals()

def logout_user(request, template_name='registration/logged_out.html'):
	auth_logout(request)
	return render(request, template_name, locals())

@view_permission
@http_response
def password_change(request, template_name='registration/password_change_form.html', password_change_form=PasswordChangeForm):
	if request.method == "POST":
		form = password_change_form(user=request.user, data=request.POST)
		if not form.is_valid():
			status = 'error'
			message = u'表單驗證失敗' +str(form.errors)
			return locals()
		form.save()
		# Updating the password logs out all other sessions for the user
		# except the current one if
		# django.contrib.auth.middleware.SessionAuthenticationMiddleware
		# is enabled.
		update_session_auth_hash(request, form.user)
		status = 'success'
		message = u'成功修改密碼'
		redirect_to = reverse('genericUser:info')
		return locals()
	if request.method == "GET":
		form = password_change_form(user=request.user)
		return locals()

def readme(request, app_name, template_name):
	template_name = app_name +'/' +template_name +'_readme.html'
	return render(request, template_name, locals())

import locale
import sys

def view_locale(request):
	loc_info = "getlocale: " + str(locale.getlocale()) + \
		"<br/>getdefaultlocale(): " + str(locale.getdefaultlocale()) + \
		"<br/>fs_encoding: " + str(sys.getfilesystemencoding()) + \
		"<br/>sys default encoding: " + str(sys.getdefaultencoding())
	return HttpResponse(loc_info)