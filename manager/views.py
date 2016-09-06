
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse
from django.http import HttpResponse,HttpResponseRedirect
from django.utils import timezone
from django.shortcuts import render, get_list_or_404
import json

from utils.decorator import *
from ebookSystem.models import *
from genericUser.models import *

@user_category_check(['manager'])
def event_list(request, action):
	if request.user.is_superuser:
		events = Event.objects.filter(content_type__model=action, status=Event.STATUS['review'])
	else:
		events = Event.objects.filter(content_type__model=action, status=Event.STATUS['review']).exclude(creater=request.user)
	template_name = 'manager/event_list_' +action +'.html'
	return render(request, template_name, locals())

@http_response
def applydocumentaction(request, template_name='manager/applydocumentaction.html'):
	if request.method == 'POST':
		ISBN = request.POST['ISBN']
		username = request.POST['username']
		events = Event.objects.filter(creater__username=username, content_type__model='applydocumentaction', status=Event.STATUS['review'])
		event_list = []
		for event in events:
			if event.action.book_info.ISBN == ISBN:
				event_list.append(event)
		if len(event_list) >= 1:
			redirect_to = event_list[0].get_url()
			status = u'success'
			message = u'代掃申請項目獲取成功'
		else:
			status = u'error'
			message = u'無此代掃申請項目'
		return locals()
	if request.method == 'GET':
		return locals()