# coding: utf-8
from django.shortcuts import render

# Create your views here.
from django.core.urlresolvers import reverse, resolve
from django.db.models import F,Q
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import generic
from ebookSystem.models import *
from genericUser.models import Event
from utils.decorator import *
import datetime
GET_MAX_PART = 3

@http_response
def sc_service(request, template_name='account/sc_service.html'):
	sc_editingPartList = request.user.sc_edit_ebook_set.all().filter(status=EBook.STATUS['sc_edit'])
	if request.method == 'POST':
		if request.POST.has_key('getPart'):
			if len(sc_editingPartList)>=3:
				status = 'error'
				message = u'您已有超過3段文件，請先校對完成再領取'
				return locals()
			try:
				getPart = EBook.objects.filter(status=EBook.STATUS['finish']).order_by('get_date')[0]
			except BaseException as e:
				status = 'error'
				message = u'無文件'
				return locals()
			getPart.change_status(1, 'sc_edit', user=request.user)
			status = 'success'
			message = u'成功取得文件{}'.format(getPart.__unicode__())
		elif request.POST.has_key('rebackPart'):
			ISBN_part = request.POST.get('rebackPart')
			rebackPart=EBook.objects.get(ISBN_part = ISBN_part)
			rebackPart.change_status(-1, 'finish')
			status = 'success'
			message = u'成功歸還文件{}'.format(rebackPart.__unicode__())
		sc_editingPartList = request.user.sc_edit_ebook_set.all().filter(status=EBook.STATUS['sc_edit'])
		return locals()
	if request.method == 'GET':
		return locals()

@http_response
def an_service(request, template_name='account/an_service.html'):
	an_editingPartList = request.user.an_edit_ebook_set.all().filter(status=EBook.STATUS['an_edit'])
	if request.method == 'POST':
		if request.POST.has_key('getPart'):
			if len(an_editingPartList)>=10:
				status = 'error'
				message = u'您已有超過10段文件，請先校對完成再領取'
				return locals()
			try:
				getPart = EBook.objects.filter(status=EBook.STATUS['sc_finish']).order_by('get_date')[0]
			except:
				status = u'error'
				message = u'無文件'
				return locals()
			getPart.change_status(1, 'an_edit', user=request.user)
			status = 'success'
			message = u'成功取得文件{}'.format(getPart.__unicode__())
		elif request.POST.has_key('rebackPart'):
			ISBN_part = request.POST.get('rebackPart')
			rebackPart=EBook.objects.get(ISBN_part = ISBN_part)
			rebackPart.change_status(-1, 'sc_finish')
			status = 'success'
			message = u'成功歸還文件{}'.format(rebackPart.__unicode__())
		an_editingPartList = request.user.an_edit_ebook_set.all().filter(status=EBook.STATUS['an_edit'])
		return locals()
	if request.method == 'GET':
		return locals()
