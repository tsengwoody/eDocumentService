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

def home(request, template_name='routing.html'):
	from django.contrib.auth import logout
	from django.http import HttpResponse, HttpResponseRedirect
	logout(request)
	return HttpResponseRedirect('/front')
	app = 'mysite'
	page = 'home'
	return render(request, template_name, locals())
