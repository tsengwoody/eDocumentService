# coding: utf-8
from django.contrib.auth import (login as auth_login, logout as auth_logout, update_session_auth_hash, authenticate,)
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.core.urlresolvers import reverse, resolve
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone
from .forms import *
from ebookSystem.models import *
from genericUser.models import *
from utils.uploadFile import *
from utils.decorator import *
from utils.other import *
from mysite.settings import BASE_DIR
import datetime
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
def dev(request, name, pk=None):
	template_name='dev/{0}.html'.format(name.split('/')[0])
	status = 'success'
	message = ''
	return locals()

@http_response
def about(request, name):
	template_name='about/{0}.html'.format(name)
	return locals()

@http_response
def home(request, template_name='home.html'):
#	logger.info('{}/home\t{}'.format(resolve(request.path).namespace, request.user))
	deadline = timezone.now() -datetime.timedelta(days=60)
	announcement_list = Announcement.objects.filter(datetime__gt=deadline).order_by('-datetime')
	return locals()

@http_response
def sitemap(request, template_name='sitemap.html'):
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

		if request.POST['role'] == 'Editor':
			try:
				newUser.is_editor = True
			except:
				newUser.delete()
				status = 'error'
				message = u'editor申請失敗'
				return locals()
		elif request.POST['role'] == 'Guest':
			try:
				DCDir = BASE_DIR +'/static/ebookSystem/disability_card/{0}'.format(newUser.username)
				handle_uploaded_file(os.path.join(DCDir, request.POST['username'] + '_front.jpg'), request.FILES['disability_card_front'])
				handle_uploaded_file(os.path.join(DCDir, request.POST['username'] + '_back.jpg'), request.FILES['disability_card_back'])
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
		message = u'資料填寫成功，需完成電子信箱與聯絡電話驗證才算完成註冊'
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
	if request.method == 'GET':
		form = authentication_form(request)
		return locals()
	if request.method == 'POST':
		form = authentication_form(request, data=request.POST)
		if not form.is_valid():
			status = 'error'
			message = u'帳號或密碼錯誤，請重新輸入'
			message = u'表單驗證失敗，' + str(form.errors)
			return locals()

		auth_login(request, form.get_user())
		if not request.user.is_license:
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

@http_response
def password_change(request, template_name='registration/password_change_form.html', password_change_form=PasswordChangeForm):
	if request.method == "POST":
		form = password_change_form(user=request.user, data=request.POST)
		if not form.is_valid():
			status = 'error'
			message = u'舊密碼或新密碼輸入錯誤'
#			message = u'表單驗證失敗' +str(form.errors)
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

@http_response
def error_social_auth(request, template_name='error_social_auth.html'):
	return locals()