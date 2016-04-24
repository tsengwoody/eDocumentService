# coding: utf-8
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.views import login as auth_login
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse
from django.db.models import F,Q
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import generic
from ebookSystem.models import *
from .forms import *
from mysite.settings import PREFIX_PATH,INACTIVE, ACTIVE, EDIT, REVIEW, REVISE, FINISH
from utils.decorator import *
import datetime
import json

MANAGER = ['tsengwoody@yahoo.com.tw']
SERVICE = 'tsengwoody.tw@gmail.com'

class profileView(generic.View):
	template_name=''

	@method_decorator(user_category_check(['editor']))
	def get(self, request, *args, **kwargs):
		readmeUrl = reverse('account:profile') +'readme/'
		template_name=self.template_name
		user=request.user
		editingPartList=EBook.objects.filter(editor=user.editor, status=EDIT)
		finishPartList=EBook.objects.filter(editor=user.editor).filter(Q(status=FINISH) | Q(status=REVIEW))
		editing = False
		if user.online:
			delta = timezone.now() - user.online
			if delta.seconds <50:
				editing = True
		return render(request, template_name, locals())

	@method_decorator(user_category_check(['editor']))
	def post(self, request, *args, **kwargs):
		readmeUrl = reverse('account:profile') +'readme/'
		template_name=self.template_name
		user=request.user
		editingPartList=EBook.objects.filter(editor=user.editor, status=EDIT)
		finishPartList=EBook.objects.filter(editor=user.editor).filter(Q(status=FINISH) | Q(status=REVIEW))
		response = {}
		redirect_to = None
		if request.POST.has_key('getPart'):
			if len(editingPartList)>3:
				response['status'] = 'error'
				response['message'] = u'您已有超過3段文件，請先校對完成再領取'
				editingPartList=EBook.objects.filter(editor=user.editor, status=EDIT)
				finishPartList=EBook.objects.filter(editor=user.editor).filter(Q(status=FINISH) | Q(status=REVIEW))
				status = response['status']
				message = response['message']
				if request.is_ajax():
					return HttpResponse(json.dumps(response), content_type="application/json")
				else:
					return render(request, template_name, locals())
			activeBook = Book.objects.filter(is_active = True).order_by('upload_date')
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
				response['status'] = 'error'
				response['message'] = u'無文件'
				editingPartList=EBook.objects.filter(editor=user.editor, status=EDIT)
				finishPartList=EBook.objects.filter(editor=user.editor).filter(Q(status=FINISH) | Q(status=REVIEW))
				status = response['status']
				message = response['message']
				if request.is_ajax():
					return HttpResponse(json.dumps(response), content_type="application/json")
				else:
					return render(request, template_name, locals())
			getPart = partialBook.ebook_set.filter(status=ACTIVE, editor=None)[0]
			getPart.editor = request.user.editor
			getPart.get_date = timezone.now()
			getPart.deadline = getPart.get_date + datetime.timedelta(days=3)
			getPart.status = EDIT
			getPart.save()
			response['status'] = 'success'
			response['message'] = u'成功取得文件{}'.format(getPart.__unicode__())
		elif request.POST.has_key('getCompleteBook'):
			if len(editingPartList)>3:
				response['status'] = 'error'
				response['message'] = u'您已有超過3段文件，請先校對完成再領取'
				editingPartList=EBook.objects.filter(editor=user.editor, status=EDIT)
				finishPartList=EBook.objects.filter(editor=user.editor).filter(Q(status=FINISH) | Q(status=REVIEW))
				status = response['status']
				message = response['message']
				if request.is_ajax():
					return HttpResponse(json.dumps(response), content_type="application/json")
				else:
					return render(request, template_name, locals())
			activeBook = Book.objects.filter(is_active = True).order_by('upload_date')
			completeBook = None
			for book in activeBook:
				if book.collect_get_count() == 0:
					completeBook = book
					break
			if not completeBook:
				response['status'] = 'error'
				response['message'] = u'目前無完整文件，請先領部份文件'
				editingPartList=EBook.objects.filter(editor=user.editor, status=EDIT)
				finishPartList=EBook.objects.filter(editor=user.editor).filter(Q(status=FINISH) | Q(status=REVIEW))
#				exchangedPartList=EBook.objects.filter(editor=user.editor, is_exchange=True)
				status = response['status']
				message = response['message']
				if request.is_ajax():
					return HttpResponse(json.dumps(response), content_type="application/json")
				else:
					return render(request, template_name, locals())
			for getPart in completeBook.ebook_set.all():
				getPart.editor = request.user.editor
				getPart.get_date = timezone.now()
				getPart.deadline = getPart.get_date + datetime.timedelta(days=3)
				getPart.status = EDIT
				getPart.save()
			response['status'] = 'success'
			response['message'] = u'成功取得完整文件{}'.format(getPart.book.__unicode__())
		elif request.POST.has_key('rebackPart'):
#			book_ISBN = request.POST.get('rebackPart').split('-')[0]
#			book_ISBN = request.POST.keys()[request.POST.values().index(u'還文件')].split('-')[0]
#			part_part = request.POST.get('rebackPart').split('-')[1]
#			part_part = request.POST.keys()[request.POST.values().index(u'還文件')].split('-')[1]
			ISBN_part = request.POST.get('rebackPart')
			rebackPart=EBook.objects.get(ISBN_part = ISBN_part)
			rebackPart.editor=None
			rebackPart.get_date = None
			rebackPart.deadline = None
			rebackPart.status = ACTIVE
			rebackPart.save()
			response['status'] = 'success'
			response['message'] = u'成功歸還文件{}'.format(rebackPart.__unicode__())
		elif request.POST.has_key('delay'):
			ISBN_part = request.POST.get('delay')
			delayPart = EBook.objects.get(ISBN_part = ISBN_part)
			delayPart.deadline = delayPart.deadline + datetime.timedelta(days=2)
			delayPart.save()
			response['status'] = 'success'
			response['message'] = u'成功延期文件{}'.format(delayPart.__unicode__())
		elif request.POST.has_key('reEditPart'):
			ISBN_part = request.POST.get('reEditPart')
			reEditPart = EBook.objects.get(ISBN_part = ISBN_part)
			reEditPart.status = EDIT
			reEditPart.save()
			response['status'] = 'success'
			response['message'] = u'再編輯文件{}'.format(reEditPart.__unicode__())
		elif request.POST.has_key('exchange'):
			ISBN_part = request.POST.get('exchange')
			exchangePart = EBook.objects.get(ISBN_part = ISBN_part)
			exchangePart.is_exchange = True
			exchangePart.save()
			response['status'] = 'success'
			response['message'] = u'已對換時數{}'.format(exchangePart.service_hours)
			editingPartList=EBook.objects.filter(editor=user.editor, status=EDIT)
			finishPartList=EBook.objects.filter(editor=user.editor).filter(Q(status=FINISH) | Q(status=REVIEW))
#			exchangedPartList=EBook.objects.filter(editor=user.editor, is_exchange=True)
		status = response['status']
		message = response['message']
		if request.is_ajax():
			return HttpResponse(json.dumps(response), content_type="application/json")
		else:
			return render(request, template_name, locals())

def readme(request, template_name):
	template_name = 'account/' +template_name +'_readme.html'
	return render(request, template_name, locals())

def static(request, template_name):
	template_name = 'account/' +template_name +'.html'
	return render(request, template_name, locals())