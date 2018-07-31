# coding: utf-8
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.core.cache import cache
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse
from django.forms import modelform_factory
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_list_or_404, redirect
from django.template.loader import get_template
from django.template import Context
from django.utils import timezone
from ebookSystem.models import *
from ebookSystem.apis import *
from genericUser.models import *
from utils.decorator import *
from utils.tag import *
from utils.uploadFile import handle_uploaded_file
from .forms import *
from mysite.settings import BASE_DIR, SERVICE, MANAGER, OTP_ACCOUNT, OTP_PASSWORD
from utils.resource import *
from zipfile import ZipFile
import base64
import json
import shutil
import datetime
import requests
import urllib, urllib2

@http_response
def generics(request, name, pk=None):
	template_name='genericUser/{0}.html'.format(name.split('/')[0])
	return locals()

@http_response
def retrieve_password(request, template_name='genericUser/retrieve_password.html'):
	if request.method == 'POST':
		print request.POST['rpw_email']
		if not request.POST['username']=='':
			try:
				birthday = request.POST['rpw_birthday'].split('-')
				birthday = [ int(i) for i in birthday ]
				birthday = datetime.date(birthday[0], birthday[1], birthday[2])
				user = User.objects.get(username=request.POST['username'], email=request.POST['rpw_email'], birthday=birthday)
			except:
				status = 'error'
				message = u'無法取得使用者資料，請確認填寫的資料是否無誤'
				return locals()
			import random
			import string
			reset_password = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
			user.set_password(reset_password)
			try:
				subject = u'重設密碼郵件'
				message = u'您的新密碼為：{0}'.format(reset_password)
				user.email_user(subject=subject, message=message)
			except:
				status = 'error'
				message = u'傳送郵件失敗'
				return locals()
			user.save()
			status = 'success'
			message = u'成功重設密碼，請至信箱取得'
			redirect_to = reverse('login')
			return locals()
		else:
			try:
				birthday = request.POST['rusr_birthday'].split('-')
				birthday = [ int(i) for i in birthday ]
				birthday = datetime.date(birthday[0], birthday[1], birthday[2])
				user = User.objects.get(email=request.POST['rusr_email'], birthday=birthday)
			except:
				status = 'error'
				message = u'無法取得使用者資料，請確認填寫的資料是否無誤'
				return locals()
			try:
				subject = u'取得username郵件'
				message = u'您的username為：{0}'.format(user.username)
				user.email_user(subject=subject, message=message)
			except:
				status = 'error'
				message = u'傳送郵件失敗'
				return locals()
			status = 'success'
			message = u'已將帳號使用者名稱寄至註冊信箱'
			return locals()
	if request.method == 'GET':
		return locals()

def user_guide(request, template_name='genericUser/user_guide.html'):
	return render(request, template_name, locals())

def recruit(request, template_name='genericUser/recruit.html'):
	return render(request, template_name, locals())

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

def event_list(request, template_name = 'genericUser/event_list.html'):
	events = Event.objects.filter(creater=request.user)
	return render(request, template_name, locals())

@http_response
def org_info(request, template_name='genericUser/org_info.html'):
	org_list = Organization.objects.filter(is_service_center=True)
	if request.method == 'POST':
		return locals()
	if request.method == 'GET':
		return locals()

def func_desc(request, template_name='genericUser/func_desc.html'):
	return render(request, template_name, locals())

@user_category_check(['manager'])
@http_response
def review_user(request, username, template_name='genericUser/review_user.html'):
	try:
		user = User.objects.get(username=username)
	except:
		raise Http404("user does not exist")
	events = Event.objects.filter(content_type__model='user', object_id=user.id, status=Event.STATUS['review'])
	sourcePath = BASE_DIR + '/static/ebookSystem/disability_card/{0}'.format(user.username)
	DCDir = BASE_DIR + '/static/ebookSystem/disability_card/{0}'.format(user.username)
	DCDir_url = DCDir.replace(BASE_DIR + '/static/', '')
	if request.method == 'GET':
		return locals()
	if request.method == 'POST':
		for item in ['active', 'editor', 'guest', 'manager', 'advanced_editor', ]:
			exec("user.is_{0} = True if request.POST.has_key('{0}') else False".format(item))
		if request.POST['review'] == 'success':
			user.status = user.STATUS['active']
			user.save()
			redirect_to = reverse('manager:event_list', kwargs={'action': 'user'})
			status = 'success'
			message = u'完成審核權限開通'
			for event in events:
				event.response(status=status, message=message, user=request.user)
		elif request.POST['review'] == 'error':
			redirect_to = reverse('manager:event_list', kwargs={'action': 'user'})
			status = 'success'
			message = u'資料異常退回'
			for event in events:
				event.response(status='error', message=request.POST['reason'], user=request.user)
		return locals()

'''subject = u'[通知] {0} 申請服務時數'.format(request.user.username)
	t = get_template('email/serviceinfo_list.txt')
	body = t.render(Context(locals()))
	email = EmailMessage(subject=subject, body=body, from_email=SERVICE, to=[exchange_serviceInfo.org.email])
	email.send(fail_silently=False)'''
