# coding: utf-8
from django.shortcuts import render

import base64
import datetime
import json
import os

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

def routing(request, name):
	app = name.split('/')[0]
	page = name.split('/')[1]
	component_page = '<{0}></{0}>'.format(page)
	template_name='routing.html'
	return render(request, template_name, locals())

def generics(request, name, pk=None):
	template_name='mysite/{0}.html'.format(name.split('/')[0])
	return render(request, template_name, locals())

def epub_view(request, path, template_name='mysite/epub_view.html'):
	#path = '/file/' +path.encode('utf8')
	path = '/api/ddm/resource/107/' +path.encode('utf8')
	base64_path = base64.b64encode(path)
	return render(request, template_name, locals())

def home(request, template_name='routing.html'):
	app = 'mysite'
	page = 'home'
	return render(request, template_name, locals())

def generic(request, template_name='routing.html'):
	app = 'mysite'
	page = 'generic'
	return render(request, template_name, locals())

def school(request, template_name='routing.html'):
	app = 'mysite'
	page = 'school'
	return render(request, template_name, locals())

def statistics(request, template_name='mysite/statistics.html'):
	if request.method == 'POST':
		return render(request, template_name, locals())
	if request.method == 'GET':
		from utils.other import month_gen
		from ebookSystem.models import Book
		from genericUser.models import User

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
		return render(request, template_name, locals())
