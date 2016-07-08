# coding: utf-8
from django.shortcuts import render

# Create your views here.
from django.core.urlresolvers import reverse, resolve
from django.db.models import F,Q
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import generic
from ebookSystem.models import *
from mysite.settings import PREFIX_PATH,INACTIVE, ACTIVE, EDIT, REVIEW, REVISE, FINISH
from utils.decorator import *
import datetime

class profileView(generic.View):
	template_name=''

	@method_decorator(user_category_check(['editor']))
	@method_decorator(http_response)
	def get(self, request, *args, **kwargs):
		readme_url = request.path +'readme/'
		template_name=self.template_name
		user=request.user
		editingPartList=EBook.objects.filter(editor=user.editor).filter(Q(status=EDIT) | Q(status=REVISE))
		finishPartList=EBook.objects.filter(editor=user.editor).filter(Q(status=FINISH) | Q(status=REVIEW))
		editing = False
		if user.online:
			delta = timezone.now() - user.online
			if delta.seconds <50:
				editing = True
		return locals()

	@method_decorator(user_category_check(['editor']))
	@method_decorator(http_response)
	def post(self, request, *args, **kwargs):
		readme_url = request.path +'readme/'
		template_name=self.template_name
		user=request.user
		editingPartList=EBook.objects.filter(editor=user.editor).filter(Q(status=EDIT) | Q(status=REVISE))
		finishPartList=EBook.objects.filter(editor=user.editor).filter(Q(status=FINISH) | Q(status=REVIEW))
		if request.POST.has_key('getPart'):
			if len(editingPartList)>=3:
				status = 'error'
				message = u'您已有超過3段文件，請先校對完成再領取'
				editingPartList=EBook.objects.filter(editor=user.editor, status=EDIT)
				finishPartList=EBook.objects.filter(editor=user.editor).filter(Q(status=FINISH) | Q(status=REVIEW))
				return locals()
			activeBook = Book.objects.filter(status = ACTIVE).order_by('upload_date')
			partialBook = None
			for book in activeBook:
				if 0 < book.collect_get_count() < book.part_count:
					partialBook = book
					break
			if not partialBook:
				print 'not partial book'
				for book in activeBook:
					if book.collect_get_count() == 0:
						partialBook = book
						break
			if not partialBook:
				status = 'error'
				message = u'無文件'
				editingPartList=EBook.objects.filter(editor=user.editor).filter(Q(status=EDIT) | Q(status=REVISE))
				finishPartList=EBook.objects.filter(editor=user.editor).filter(Q(status=FINISH) | Q(status=REVIEW))
				return locals()
			getPart = partialBook.ebook_set.filter(status=ACTIVE)[0]
			getPart.editor = request.user.editor
			getPart.get_date = timezone.now()
			getPart.deadline = getPart.get_date + datetime.timedelta(days=3)
			getPart.status = EDIT
			getPart.save()
			status = 'success'
			message = u'成功取得文件{}'.format(getPart.__unicode__())
		elif request.POST.has_key('getCompleteBook'):
			if len(editingPartList)>3:
				status = 'error'
				message = u'您已有超過3段文件，請先校對完成再領取'
				editingPartList=EBook.objects.filter(editor=user.editor).filter(Q(status=EDIT) | Q(status=REVISE))
				finishPartList=EBook.objects.filter(editor=user.editor).filter(Q(status=FINISH) | Q(status=REVIEW))
				return locals()
			activeBook = Book.objects.filter(status = ACTIVE).order_by('upload_date')
			completeBook = None
			for book in activeBook:
				if book.collect_get_count() == 0:
					completeBook = book
					break
			if not completeBook:
				status = 'error'
				message = u'目前無完整文件，請先領部份文件'
				editingPartList=EBook.objects.filter(editor=user.editor).filter(Q(status=EDIT) | Q(status=REVISE))
				finishPartList=EBook.objects.filter(editor=user.editor).filter(Q(status=FINISH) | Q(status=REVIEW))
				return locals()
			for getPart in completeBook.ebook_set.all():
				getPart.editor = request.user.editor
				getPart.get_date = timezone.now()
				getPart.deadline = getPart.get_date + datetime.timedelta(days=3)
				getPart.status = EDIT
				getPart.save()
			status = 'success'
			message = u'成功取得完整文件{}'.format(getPart.book.__unicode__())
		elif request.POST.has_key('rebackPart'):
			ISBN_part = request.POST.get('rebackPart')
			rebackPart=EBook.objects.get(ISBN_part = ISBN_part)
			rebackPart.editor=None
			rebackPart.get_date = None
			rebackPart.deadline = None
			rebackPart.status = ACTIVE
			rebackPart.save()
			status = 'success'
			message = u'成功歸還文件{}'.format(rebackPart.__unicode__())
		elif request.POST.has_key('reEditPart'):
			ISBN_part = request.POST.get('reEditPart')
			reEditPart = EBook.objects.get(ISBN_part = ISBN_part)
			reEditPart.status = EDIT
			reEditPart.save()
			status = 'success'
			message = u'再編輯文件{}'.format(reEditPart.__unicode__())
		elif request.POST.has_key('exchange'):
			ISBN_part = request.POST.get('exchange')
			exchangePart = EBook.objects.get(ISBN_part = ISBN_part)
			exchangePart.is_exchange = True
			exchangePart.save()
			status = 'success'
			message = u'已對換時數{}'.format(exchangePart.service_hours)
			editingPartList=EBook.objects.filter(editor=user.editor, status=EDIT)
			finishPartList=EBook.objects.filter(editor=user.editor).filter(Q(status=FINISH) | Q(status=REVIEW))
		else:
			status = 'error'
			message = u'不明的操作'
		return locals()

def readme(request, template_name):
	template_name = resolve(request.path).namespace +'/' +template_name +'_readme.html'
	return render(request, template_name, locals())
