# coding: utf-8
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse
from django.http import HttpResponse,HttpResponseRedirect
from django.utils import timezone
from django.shortcuts import render, get_list_or_404

from utils.decorator import *
from ebookSystem.models import *
from genericUser.models import *
from mysite.settings import BASE_DIR

import codecs
import os

@http_response
def statistics(request, template_name='manager/statistics.html'):
	if request.method == 'POST':
		return locals()
	if request.method == 'GET':
		from utils.other import month_gen
		month_list = month_gen(count=5)
		month_list.insert(0, datetime.datetime.today())
		result = []
		for month in month_list:
			editor_list = User.objects.filter(is_editor=True, date_joined__lte=month, auth_email=True, auth_phone=True,)
			guest_list = User.objects.filter(is_guest=True, date_joined__lte=month, auth_email=True, auth_phone=True,)
			editor_list_30 = User.objects.filter(is_editor=True, date_joined__lte=month, last_login__gt=month -datetime.timedelta(days=30), auth_email=True, auth_phone=True,)
			finish_list = Book.objects.filter(finish_date__lte=month, upload_date__lte=month, source='self')
			txt_list = Book.objects.filter(upload_date__lte=month, source='txt')
			epub_list = Book.objects.filter(upload_date__lte=month, source='epub')
			book_list = Book.objects.filter(upload_date__lte=month)
			scanbook_list = Book.objects.filter(upload_date__lte=month, source='self')
			result.append((
				month,
				len(editor_list),
				len(guest_list),
				len(editor_list_30),
				len(book_list),
				len(scanbook_list),
				len(finish_list) ,
				len(txt_list) ,
				len(epub_list),
			))
		month = datetime.date.today() -datetime.timedelta(days=30)
		active_editor_list = User.objects.filter(is_editor=True, last_login__gt=month)
		return locals()

@view_permission
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

@http_response
def org_manage(request, template_name='manager/org_manage.html'):
	if request.method == 'POST':
		if request.POST.has_key('servicehours_info'):
			pass
		elif request.POST.has_key('volunteer_info'):
			org = Organization.objects.get(id=request.POST['volunteer_info'])
			path = BASE_DIR +u'/file/organization/{0}/volunteer_information.txt'.format(request.POST['volunteer_info'])
			info = ''
			for user in org.user_set.all():
				info = info +u'{0}\t{1}\t{2}\t{3}\t{4}\r\n'.format(unicode(user), user.username, user.email, user.phone, user.birthday)
			if not os.path.exists(os.path.dirname(path)):
				os.makedirs(os.path.dirname(path), 0770)
			with codecs.open(path, 'w', encoding='utf-8') as file:
				file.write(info)
			download_path = path
			download_filename = 'volunteer_information.txt'
		return locals()
	if request.method == 'GET':
		return locals()
