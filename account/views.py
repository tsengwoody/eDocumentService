# coding: utf-8
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.views import login as auth_login
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse
from django.db.models import F
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import generic
from ebookSystem.models import *
from .forms import *
from utils.decorator import *
import datetime
import json

MANAGER = ['tsengwoody@yahoo.com.tw']
SERVICE = 'tsengwoody.tw@gmail.com'

class profileView(generic.View):
	template_name=''

	@method_decorator(user_category_check('editor'))
	def get(self, request, *args, **kwargs):
		readmeUrl = reverse('account:profile') +'readme/'
		template_name=self.template_name
		user=request.user
		editingPartList=EBook.objects.filter(editor=user.editor, is_finish=False)
		finishPartList=EBook.objects.filter(editor=user.editor,is_finish=True)
#		exchangedPartList=EBook.objects.filter(editor=user.editor,is_finish=True, is_exchange=True)
		return render(request, template_name, locals())

	@method_decorator(user_category_check('editor'))
	def post(self, request, *args, **kwargs):
		readmeUrl = reverse('account:profile') +'readme/'
		template_name=self.template_name
		print 'POST dict'
		print request.POST
		response = {'status':'', 'message':''}
		redirect_to = None
		print request;
		user=request.user
		if request.POST.has_key('getPart'):
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
				editingPartList=EBook.objects.filter(editor=user.editor, is_finish=False)
				finishPartList=EBook.objects.filter(editor=user.editor,is_finish=True)
				exchangedPartList=EBook.objects.filter(editor=user.editor,is_finish=True, is_exchange=True)
				status = response['status']
				message = response['message']
				if request.is_ajax():
					return HttpResponse(json.dumps(response), content_type="application/json")
				else:
					return render(request, template_name, locals())
			getPart = partialBook.ebook_set.filter(is_finish=False, editor=None)[0]
			getPart.editor = request.user.editor
			getPart.get_date = timezone.now()
			getPart.deadline = getPart.get_date + datetime.timedelta(days=3)
			getPart.save()
			response['status'] = 'success'
			response['message'] = u'成功取得文件{}'.format(getPart.__unicode__())
		elif request.POST.has_key('getCompleteBook'):
			activeBook = Book.objects.filter(is_active = True).order_by('upload_date')
			completeBook = None
			for book in activeBook:
				if book.collect_get_count() == 0:
					completeBook = book
					break
			if not completeBook:
				response['status'] = 'error'
				response['message'] = u'目前無完整文件，請先領部份文件'
				editingPartList=EBook.objects.filter(editor=user.editor, is_finish=False)
				finishPartList=EBook.objects.filter(editor=user.editor,is_finish=True)
				exchangedPartList=EBook.objects.filter(editor=user.editor,is_finish=True, is_exchange=True)
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
				getPart.save()
			response['status'] = 'success'
			response['message'] = u'成功取得完整文件{}'.format(getPart.book.__unicode__())
		elif request.POST.has_key('rebackPart'):
			book_ISBN = request.POST.get('rebackPart').split('-')[0]
#			book_ISBN = request.POST.keys()[request.POST.values().index(u'還文件')].split('-')[0]
			part_part = request.POST.get('rebackPart').split('-')[1]
#			part_part = request.POST.keys()[request.POST.values().index(u'還文件')].split('-')[1]
			rebackPart=EBook.objects.get(part=part_part, book__ISBN = book_ISBN)
			rebackPart.editor=None
			rebackPart.get_date = None
			rebackPart.deadline = None
			rebackPart.save()
			response['status'] = 'success'
			response['message'] = u'成功歸還文件{}'.format(rebackPart.__unicode__())
		elif request.POST.has_key('delay'):
			book_ISBN = request.POST.get('delay').split('-')[0]
			part_part = request.POST.get('delay').split('-')[1]
			delayPart = EBook.objects.get(part=part_part, book__ISBN = book_ISBN)
			delayPart.deadline = delayPart.deadline + datetime.timedelta(days=2)
			delayPart.save()
			response['status'] = 'success'
			response['message'] = u'成功延期文件{}'.format(delayPart.__unicode__())
		elif request.POST.has_key('reEditPart'):
			book_ISBN = request.POST.get('reEditPart').split('-')[0]
			part_part = request.POST.get('reEditPart').split('-')[1]
			reEditPart = EBook.objects.get(part=part_part, book__ISBN = book_ISBN)
			reEditPart.is_finish = False
			reEditPart.save()
			response['status'] = 'success'
			response['message'] = u'再編輯文件{}'.format(delayPart.__unicode__())
		elif request.POST.has_key('exchange'):
			book_ISBN = request.POST.get('exchange').split('-')[0]
			part_part = request.POST.get('exchange').split('-')[1]
			exchangePart = EBook.objects.get(part=part_part, book__ISBN = book_ISBN)
			exchangePart.is_exchange = True
			exchangePart.save()
			response['status'] = 'success'
			response['message'] = u'已對換時數{}'.format(exchangePart.service_hours)
		editingPartList=EBook.objects.filter(editor=user.editor, is_finish=False)
		finishPartList=EBook.objects.filter(editor=user.editor,is_finish=True)
		exchangedPartList=EBook.objects.filter(editor=user.editor,is_finish=True, is_exchange=True)
		status = response['status']
		message = response['message']
		if request.is_ajax():
			return HttpResponse(json.dumps(response), content_type="application/json")
		else:
			return render(request, template_name, locals())

def readme(request, template_name):
	template_name = 'account/' +template_name +'_readme.html'
	return render(request, template_name, locals())