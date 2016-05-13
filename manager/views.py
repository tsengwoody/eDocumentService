# coding: utf-8
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse
from django.http import HttpResponse,HttpResponseRedirect
from django.utils import timezone
from django.shortcuts import render, get_list_or_404
import json

from utils.decorator import *
from ebookSystem.models import *
from genericUser.models import *
from mysite.settings import PREFIX_PATH,INACTIVE, ACTIVE, EDIT, REVIEW, REVISE, FINISH

@user_category_check(['manager'])
def review_user_list(request, template_name='manager/review_user_list.html'):
	user_list = User.objects.filter(status=REVIEW)
	return render(request, template_name, locals())

@user_category_check(['manager'])
def review_document_list(request, template_name='manager/review_document_list.html'):
	book_list = Book.objects.filter(status = INACTIVE)
	return render(request, template_name, locals())

@user_category_check(['manager'])
def review_part_list(request, template_name='manager/review_part_list.html'):
	part_list = EBook.objects.filter(status=REVIEW)
	return render(request, template_name, locals())

def readme(request, template_name):
	template_name = 'manager/' +template_name +'_readme.html'
	return render(request, template_name, locals())

def static(request, template_name):
	template_name = 'account/' +template_name +'.html'
	return render(request, template_name, locals())