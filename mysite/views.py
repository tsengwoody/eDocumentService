# coding: utf-8
from django.contrib.auth import (login as auth_login, logout as auth_logout, update_session_auth_hash, authenticate,)
from django.core.urlresolvers import reverse, resolve
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone
from ebookSystem.models import *
from genericUser.models import *
from utils.decorator import *
from utils.other import *
from mysite.settings import BASE_DIR

import base64
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
def routing(request, name):
	app = name.split('/')[0]
	page = name.split('/')[1]
	component_page = '<{0}></{0}>'.format(page)
	template_name='routing.html'
	return locals()

@http_response
def generics(request, name, pk=None):
	template_name='mysite/{0}.html'.format(name.split('/')[0])
	return locals()

@http_response
def epub_view(request, path, template_name='mysite/epub_view.html'):
		path = '/file/' +path.encode('utf8')
		base64_path = base64.b64encode(path)
		return locals()

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

def logout_user(request, template_name='registration/logged_out.html'):
	auth_logout(request)
	return render(request, template_name, locals())

from utils.decorator import *

@http_response
def statistics(request, template_name='mysite/statistics.html'):
	if request.method == 'POST':
		return locals()
	if request.method == 'GET':
		from utils.other import month_gen
		month_list = month_gen(count=5)
		month_list.insert(0, datetime.datetime.today())
		result = []
		for month in month_list:
			editor_count = User.objects.filter(is_editor=True, date_joined__lte=month, auth_email=True, auth_phone=True,).count()
			guest_count = User.objects.filter(is_guest=True, date_joined__lte=month, auth_email=True, auth_phone=True,).count()
			editor_count_30 = User.objects.filter(is_editor=True, date_joined__lte=month, last_login__gt=month -datetime.timedelta(days=30), auth_email=True, auth_phone=True,).count()
			finish_count = Book.objects.filter(finish_date__lte=month, upload_date__lte=month, source='self').count()
			txt_count = Book.objects.filter(upload_date__lte=month, source='txt').count()
			epub_count = Book.objects.filter(upload_date__lte=month, source='epub').count()
			book_count = Book.objects.filter(upload_date__lte=month).count()
			scanbook_count = Book.objects.filter(upload_date__lte=month, source='self').count()
			result.append((
				month,
				editor_count,
				guest_count,
				editor_count_30,
				book_count,
				scanbook_count,
				finish_count,
				txt_count,
				epub_count,
			))
		month = datetime.date.today() -datetime.timedelta(days=30)
		active_editor_list = User.objects.filter(is_editor=True, last_login__gt=month)
		return locals()
