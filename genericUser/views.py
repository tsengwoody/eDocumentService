# coding: utf-8
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse
from django.http import HttpResponse,HttpResponseRedirect
from django.utils import timezone
from django.shortcuts import render
from ebookSystem.models import *
from ebookSystem.forms import *

MANAGER = ['tsengwoody@yahoo.com.tw']
SERVICE = 'tsengwoody.tw@gmail.com'

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