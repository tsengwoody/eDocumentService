# coding: utf-8
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse
from django.http import HttpResponse,HttpResponseRedirect
from django.utils import timezone
from django.shortcuts import render
import json

from utils.decorator import *
from .forms import *

MANAGER = ['tsengwoody@yahoo.com.tw']
SERVICE = 'tsengwoody.tw@gmail.com'

def review_user(request, username, template_name='genericUser/review_user.html'):
	try:
		user = User.objects.get(username=username)
	except:
		raise Http404("book does not exist")
	if request.method == 'GET':
		return render(request, template_name, locals())
	if request.method == 'POST':
		response = {}
		if request.POST['review'] == 'success':
			user.status = ACTIVE
			response['status'] = 'success'
			response['message'] = u'審核通過會員'
			response['redirect_to'] = reverse('manager:review_user_list')
		if request.POST['review'] == 'error':
			user.status = REVISE
			response['status'] = 'error'
			response['message'] = u'審核退回會員'
			response['redirect_to'] = reverse('manager:review_user')
		status = response['status']
		message = response['message']
		redirect_to = response['redirect_to']
		if request.is_ajax():
			return HttpResponse(json.dumps(response), content_type="application/json")
		else:
			return render(request, template_name, locals())



@user_category_check(['editor', 'guest'])
def info(request, template_name):
	user = request.user
	return render(request, template_name, locals())

@user_category_check(['editor', 'guest'])
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

def set_role(request,template_name='genericUser/set_role.html'):
#	if request.method == 'POST':
#		request.POST
	if request.method == 'GET':
		return render(request, template_name, locals())


def contact_us(request, template_name='genericUser/contact_us.html'):
	if request.method == 'GET':
		contactUsForm = ContactUsForm()
		return render(request, template_name, locals())
	if request.method == 'POST':
		response = {}
		redirect_to = None
		contactUsForm = ContactUsForm(request.POST)
		if contactUsForm.is_valid():
			contactUs = contactUsForm.save(commit=False)
			contactUs.message_datetime = timezone.now()
			subject = u'[{}] {}'.format (contactUs.kind, contactUs.subject)
			body = u'姓名:'+ contactUs.name+ u'\nemail:'+ contactUs.email+ u'\n內容：\n'+ contactUs.content
			email = EmailMessage(subject=subject, body=body, from_email=SERVICE, to=MANAGER)
			email.send(fail_silently=False)
			contactUs.save()
			redirect_to = reverse('account:profile')
			response['status'] = 'success'
			response['message'] = u'成功寄送內容，我們將盡速回復'
		else:
			response['status'] = 'error'
			response['message'] = u'表單驗證失敗'
		status = response['status']
		message = response['message']
		if request.is_ajax():
			return HttpResponse(json.dumps(response), content_type="application/json")
		else:
#			if redirect_to:
#				return HttpResponseRedirect(redirect_to)
#			else:
			return render(request, template_name, locals())

def readme(request, template_name):
	template_name = 'account/' +template_name +'_readme.html'
	return render(request, template_name, locals())