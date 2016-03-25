# coding: utf-8
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse
from django.http import HttpResponse,HttpResponseRedirect
from django.utils import timezone
from django.shortcuts import render

from utils.decorator import *
from .forms import *

MANAGER = ['tsengwoody@yahoo.com.tw']
SERVICE = 'tsengwoody.tw@gmail.com'

@user_category_check('editor')
def info(request, template_name):
	user = request.user
	return render(request, template_name, locals())

@user_category_check('editor')
def info_change(request,template_name):
	user = request.user
	if request.method == 'POST':
		infoChangeUserForm = InfoChangeUserForm(request.POST, instance = user)
		if infoChangeUserForm.is_valid():
			infoChangeUserForm.save()
			redirect_to = reverse('genericUser:info')
			return HttpResponseRedirect(redirect_to)
	if request.method == 'GET':
		infoChangeUserForm = InfoChangeUserForm(instance = user)
	return render(request, template_name, locals())

def contact_us(request, template_name):
	if request.method == 'GET':
		contactUsForm = ContactUsForm()
	if request.method == 'POST':
		contactUsForm = ContactUsForm(request.POST)
		if contactUsForm.is_valid():
			contactUs = contactUsForm.save(commit=False)
			contactUs.message_datetime = timezone.now()
			subject = u'[{}] {}'.format (contactUs.kind, contactUs.subject)
			body = u'姓名:'+ contactUs.name+ u'\nemail:'+ contactUs.email+ u'\n內容：'+ contactUs.content
			email = EmailMessage(subject=subject, body=body, from_email=SERVICE, to=MANAGER)
			email.send(fail_silently=False)
			contactUs.save()
			redirect_to = reverse('account:profile')
			return HttpResponseRedirect(redirect_to)
	return render(request, template_name, locals())