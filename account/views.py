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

class profileView(generic.View):
	template_name=''

	@method_decorator(user_category_check(['editor']))
	@method_decorator(http_response)
	def get(self, request, *args, **kwargs):
		readme_url = request.path +'readme/'
		template_name=self.template_name
		editingPartList = request.user.edit_ebook_set.all().filter(status=EBook.STATUS['edit'])
		finishPartList = request.user.edit_ebook_set.all().filter(status__gte=EBook.STATUS['review'])
		return locals()

	@method_decorator(user_category_check(['editor']))
	@method_decorator(http_response)
	def post(self, request, *args, **kwargs):
		readme_url = request.path +'readme/'
		template_name=self.template_name
		editingPartList = request.user.edit_ebook_set.all().filter(status=EBook.STATUS['edit'])
		finishPartList = request.user.edit_ebook_set.all().filter(status__gte=EBook.STATUS['review'])
		if request.POST.has_key('getPart'):
			if len(editingPartList)>=10:
				status = 'error'
				message = u'您已有超過10段文件，請先校對完成再領取'
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
			getPart.editor = request.user
			getPart.get_date = timezone.now()
			getPart.deadline = getPart.get_date + datetime.timedelta(days=5)
			getPart.status = getPart.STATUS['edit']
			getPart.save()
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
				getPart.editor = request.user
				getPart.get_date = timezone.now()
				getPart.deadline = getPart.get_date + datetime.timedelta(days=5)
				getPart.status = getPart.STATUS['edit']
				getPart.save()
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
			getPart.editor = request.user
			getPart.get_date = timezone.now()
			getPart.deadline = getPart.get_date + datetime.timedelta(days=5)
			getPart.status = getPart.STATUS['edit']
			getPart.save()
			status = 'success'
			message = u'成功取得指定文件{}'.format(getPart.book.__unicode__())
		elif request.POST.has_key('rebackPart'):
			ISBN_part = request.POST.get('rebackPart')
			rebackPart=EBook.objects.get(ISBN_part = ISBN_part)
			rebackPart.editor=None
			rebackPart.get_date = None
			rebackPart.deadline = None
			rebackPart.status = rebackPart.STATUS['active']
			rebackPart.save()
			status = 'success'
			message = u'成功歸還文件{}'.format(rebackPart.__unicode__())
		elif request.POST.has_key('reEditPart'):
			ISBN_part = request.POST.get('reEditPart')
			reEditPart = EBook.objects.get(ISBN_part = ISBN_part)
			reEditPart.status = reEditPart.STATUS['edit']
			reEditPart.load_full_content()
			events = Event.objects.filter(content_type__model='ebook', object_id=reEditPart.ISBN_part, status=Event.STATUS['review'])
			for event in events:
				event.delete()
			reEditPart.save()
			status = 'success'
			message = u'再編輯文件{}'.format(reEditPart.__unicode__())
		else:
			status = 'error'
			message = u'不明的操作'
		editingPartList = request.user.edit_ebook_set.all().filter(status=EBook.STATUS['edit'])
		finishPartList = request.user.edit_ebook_set.all().filter(status__gte=EBook.STATUS['review'])
		return locals()

@http_response
def sc_service(request, template_name='account/sc_service.html'):
	sc_editingPartList = request.user.sc_edit_ebook_set.all().filter(status=EBook.STATUS['sc_edit'])
	sc_finishPartList = request.user.sc_edit_ebook_set.all().filter(status=EBook.STATUS['sc_finish'])
	if request.method == 'POST':
		if request.POST.has_key('getPart'):
			if len(sc_editingPartList)>=10:
				status = 'error'
				message = u'您已有超過10段文件，請先校對完成再領取'
				return locals()
			try:
				getPart = EBook.objects.filter(status=EBook.STATUS['finish']).order_by('get_date')[0]
			except:
				status = u'error'
				message = u'無文件'
				return locals()
			getPart.sc_editor = request.user
			getPart.sc_get_date = timezone.now()
			if getPart.is_sc_rebuild:
				getPart.create_SpecialContent()
				getPart.is_sc_rebuild = False
			getPart.status = getPart.STATUS['sc_edit']
			getPart.save()
			status = 'success'
			message = u'成功取得文件{}'.format(getPart.__unicode__())
		elif request.POST.has_key('rebackPart'):
			ISBN_part = request.POST.get('rebackPart')
			rebackPart=EBook.objects.get(ISBN_part = ISBN_part)
			rebackPart.sc_editor=None
			rebackPart.sc_get_date = None
			rebackPart.status = rebackPart.STATUS['finish']
			rebackPart.save()
			status = 'success'
			message = u'成功歸還文件{}'.format(rebackPart.__unicode__())
		sc_editingPartList = request.user.sc_edit_ebook_set.all().filter(status=EBook.STATUS['sc_edit'])
		sc_finishPartList = request.user.sc_edit_ebook_set.all().filter(status=EBook.STATUS['sc_finish'])
		return locals()
	if request.method == 'GET':
		return locals()

@http_response
def an_service(request, template_name='account/an_service.html'):
	an_editingPartList = request.user.analyze_ebook_set.all().filter(status=EBook.STATUS['an_edit'])
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
			getPart.analyze_editor = request.user
			getPart.an_get_date = timezone.now()
			getPart.status = getPart.STATUS['an_edit']
			getPart.save()
			status = 'success'
			message = u'成功取得文件{}'.format(getPart.__unicode__())
		elif request.POST.has_key('rebackPart'):
			ISBN_part = request.POST.get('rebackPart')
			rebackPart=EBook.objects.get(ISBN_part = ISBN_part)
			rebackPart.analyze_editor=None
			rebackPart.an_get_date = None
			rebackPart.status = rebackPart.STATUS['sc_finish']
			rebackPart.save()
			status = 'success'
			message = u'成功歸還文件{}'.format(rebackPart.__unicode__())
		an_editingPartList = request.user.analyze_ebook_set.all().filter(status=EBook.STATUS['an_edit'])
		return locals()
	if request.method == 'GET':
		return locals()

def readme(request, template_name):
	template_name = resolve(request.path).namespace +'/' +template_name +'_readme.html'
	return render(request, template_name, locals())
