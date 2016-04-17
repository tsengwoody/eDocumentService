# coding: utf-8
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse
from django.http import HttpResponse,HttpResponseRedirect
from django.utils import timezone
from django.shortcuts import render
import json

from utils.decorator import *
from ebookSystem.models import *
from genericUser.models import *

#@user_category_check('editor')
def review_user_list(request, template_name='manager/review_user_list.html'):
	user_list = User.objects.filter(is_review = False)
	return render(request, template_name, locals())

def review_document_list(request, template_name='manager/review_document_list.html'):
	book_list = Book.objects.filter(is_active = False)
	return render(request, template_name, locals())

def readme(request, template_name):
	template_name = 'manager/' +template_name +'_readme.html'
	return render(request, template_name, locals())

def static(request, template_name):
	template_name = 'account/' +template_name +'.html'
	return render(request, template_name, locals())