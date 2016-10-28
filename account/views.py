# coding: utf-8
from django.shortcuts import render

# Create your views here.
from django.core.urlresolvers import reverse, resolve
from django.db.models import F,Q
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import generic
from ebookSystem.models import *
from genericUser.models import Event, ServiceHours
from utils.decorator import *
import datetime
GET_MAX_PART = 3

@user_category_check(['editor'])
@http_response
def service(request, template_name='account/service.html'):
	editingPartList = request.user.edit_ebook_set.all().filter(status=EBook.STATUS['edit'])
	finishPartList = request.user.edit_ebook_set.all().filter(status__gte=EBook.STATUS['review'])
	if request.method == 'POST':
		if request.POST.has_key('getPart'):
			if len(editingPartList)>=GET_MAX_PART:
				status = 'error'
				message = u'您已有超過{0}段文件，請先校對完成再領取'.format(GET_MAX_PART)
				return locals()
			activeBook = Book.objects.filter(Q(status=Book.STATUS['active']) & Q(is_private=False)).order_by('upload_date')
			partialBook = None
			for book in activeBook:
				if 0 < book.collect_get_count() < book.part_count:
					partialBook = book
					break
			if not partialBook:
				for book in activeBook:
					if book.collect_get_count() == 0:
						partialBook = book
						break
			if not partialBook:
				status = 'error'
				message = u'無文件'
				return locals()
			getPart = partialBook.ebook_set.filter(status=EBook.STATUS['active']).order_by('part')[0]
			getPart.change_status(1, 'edit', user=request.user)
			status = 'success'
			message = u'成功取得文件{}'.format(getPart.__unicode__())
		elif request.POST.has_key('getCompleteBook'):
			if len(editingPartList)>10:
				status = 'error'
				message = u'您已有超過10段文件，請先校對完成再領取'
				return locals()
			activeBook = Book.objects.filter(Q(status=Book.STATUS['active']) & Q(is_private=False)).order_by('upload_date')
			completeBook = None
			for book in activeBook:
				if book.collect_get_count() == 0:
					completeBook = book
					break
			if not completeBook:
				status = 'error'
				message = u'目前無完整文件，請先領部份文件'
				return locals()
			for getPart in completeBook.ebook_set.all():
				getPart.change_status(1, 'edit', user=request.user)
			status = 'success'
			message = u'成功取得完整文件{}'.format(getPart.book.__unicode__())
		elif request.POST.has_key('designateBook'):
			if len(editingPartList)>10:
				status = 'error'
				message = u'您已有超過10段文件，請先校對完成再領取'
				return locals()
			if request.POST.has_key('ISBN'):
				activeBook = Book.objects.filter(ISBN=request.POST['ISBN'])
			if request.POST.has_key('username'):
				activeBook = Book.objects.filter(owner__username=request.POST['username'])
			partialBook = None
			for book in activeBook:
				if 0 < book.collect_get_count() < book.part_count:
					partialBook = book
					break
			if not partialBook:
				for book in activeBook:
					if book.collect_get_count() == 0:
						partialBook = book
						break
			if not partialBook:
				status = 'error'
				message = u'無文件'
				return locals()
			getPart = partialBook.ebook_set.filter(status=EBook.STATUS['active']).order_by('part')[0]
			getPart.change_status(1, 'edit', user=request.user)
			status = 'success'
			message = u'成功取得指定文件{}'.format(getPart.book.__unicode__())
		elif request.POST.has_key('rebackPart'):
			ISBN_part = request.POST.get('rebackPart')
			rebackPart=EBook.objects.get(ISBN_part = ISBN_part)
			rebackPart.change_status(-1, 'active', user=request.user)
			status = 'success'
			message = u'成功歸還文件{}'.format(rebackPart.__unicode__())
		elif request.POST.has_key('reEditPart'):
			ISBN_part = request.POST.get('reEditPart')
			reEditPart = EBook.objects.get(ISBN_part = ISBN_part)
			reEditPart.change_status(-1, 'edit')
			events = Event.objects.filter(content_type__model='ebook', object_id=reEditPart.ISBN_part, status=Event.STATUS['review'])
			for event in events:
				event.delete()
			status = 'success'
			message = u'再編輯文件{}'.format(reEditPart.__unicode__())
		else:
			status = 'error'
			message = u'不明的操作'
		editingPartList = request.user.edit_ebook_set.all().filter(status=EBook.STATUS['edit'])
		finishPartList = request.user.edit_ebook_set.all().filter(status__gte=EBook.STATUS['review'])
		return locals()
	if request.method == 'GET':
		return locals()

@user_category_check(['advanced_editor'])
@http_response
def sc_service(request, template_name='account/sc_service.html'):
	sc_editingPartList = request.user.sc_edit_ebook_set.all().filter(Q(status=EBook.STATUS['sc_edit']))
	if request.method == 'POST':
		if request.POST.has_key('getPart'):
			if len(sc_editingPartList)>=10:
				status = 'error'
				message = u'您已有超過10段文件，請先校對完成再領取'
				return locals()
			try:
				getPart = EBook.objects.filter(Q(status=EBook.STATUS['finish']) & Q(book__is_private=False)).order_by('get_date')[0]
			except:
				status = u'error'
				message = u'無文件'
				return locals()
			getPart.change_status(1, 'sc_edit', user=request.user)
			status = 'success'
			message = u'成功取得文件{}'.format(getPart.__unicode__())
		elif request.POST.has_key('designateBook'):
			if len(sc_editingPartList)>10:
				status = 'error'
				message = u'您已有超過10段文件，請先校對完成再領取'
				return locals()
			activeBook = None
			if request.POST.has_key('ISBN'):
				activeBook = Book.objects.filter(ISBN=request.POST['ISBN'])
			elif request.POST.has_key('username'):
				activeBook = Book.objects.filter(owner__username=request.POST['username'])
			if not activeBook:
				status = 'error'
				message = u'無指定文件'
				return locals()
			partialBook = None
			for book in activeBook:
				if 0 < book.collect_get_count() < book.part_count:
					partialBook = book
					break
			if not partialBook:
				for book in activeBook:
					if book.collect_get_count() == 0:
						partialBook = book
						break
			if not partialBook:
				status = 'error'
				message = u'無文件'
				return locals()
			getPart = partialBook.ebook_set.filter(status=EBook.STATUS['finish']).order_by('part')[0]
			getPart.change_status(1, 'sc_edit', user=request.user)
			status = 'success'
			message = u'成功取得指定文件{}'.format(getPart.book.__unicode__())
		elif request.POST.has_key('rebackPart'):
			ISBN_part = request.POST.get('rebackPart')
			rebackPart=EBook.objects.get(ISBN_part = ISBN_part)
			rebackPart.change_status(-1, 'finish')
			status = 'success'
			message = u'成功歸還文件{}'.format(rebackPart.__unicode__())
		sc_editingPartList = request.user.sc_edit_ebook_set.all().filter(Q(status=EBook.STATUS['sc_edit']))
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

@http_response
def readme(request, template_name):
	template_name = resolve(request.path).namespace +'/' +template_name +'_readme.html'
	return render(request, template_name, locals())
