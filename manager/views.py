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
def event_list(request, action):
	events = Event.objects.filter(content_type__model=action, status=-1)
	template_name = 'manager/event_list_' +action +'.html'
	return render(request, template_name, locals())
