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

MANAGER = ['tsengwoody@yahoo.com.tw']
SERVICE = 'tsengwoody.tw@gmail.com'

@user_category_check('editor')
def info(request,template_name='account/info.html'):
	user = request.user
	return render(request, template_name, locals())

@user_category_check('editor')
def info_change(request,template_name='account/info_change.html'):
	user = request.user
	if request.method == 'POST':
		infoChangeUserForm = InfoChangeUserForm(request.POST, instance = user)
		if infoChangeUserForm.is_valid():
			infoChangeUserForm.save()
			redirect_to = reverse('account:info')
			return HttpResponseRedirect(redirect_to)
	if request.method == 'GET':
		infoChangeUserForm = InfoChangeUserForm(instance = user)
	return render(request, template_name, locals())

@user_category_check('editor')
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

class profileView(generic.View):
	template_name=''

	@method_decorator(user_category_check('editor'))
	def get(self, request, *args, **kwargs):
		template_name=self.template_name
		user=request.user
		editingPartList=EBook.objects.filter(editor=user.editor, is_finish=False)
		finishPartList=EBook.objects.filter(editor=user.editor,is_finish=True, is_exchange=False)
		exchangedPartList=EBook.objects.filter(editor=user.editor,is_finish=True, is_exchange=True)
		return render(request, template_name, locals())

	@method_decorator(user_category_check('editor'))
	def post(self, request, *args, **kwargs):
		template_name=self.template_name
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
				error_message = u'無文件'
				print 'not book'
				editingPartList=EBook.objects.filter(editor=user.editor, is_finish=False)
				finishPartList=EBook.objects.filter(editor=user.editor,is_finish=True)
				exchangedPartList=EBook.objects.filter(editor=user.editor,is_finish=True, is_exchange=True)
				return render(request, template_name, locals())
			getPart = partialBook.ebook_set.filter(is_finish=False, editor=None)[0]
			print 'get part'+getPart.__unicode__()
			getPart.editor = request.user.editor
			getPart.get_date = timezone.now()
			getPart.deadline = getPart.get_date + datetime.timedelta(days=3)
			getPart.save()
		elif request.POST.has_key('getCompleteBook'):
			activeBook = Book.objects.filter(is_active = True).order_by('upload_date')
			completeBook = None
			for book in activeBook:
				if book.collect_get_count() == 0:
					completeBook = book
					break
			if not completeBook:
				error_message = u'目前無完整書文件，請先領部份文件'
				print 'not Complete book'
				editingPartList=EBook.objects.filter(editor=user.editor, is_finish=False)
				finishPartList=EBook.objects.filter(editor=user.editor,is_finish=True)
				exchangedPartList=EBook.objects.filter(editor=user.editor,is_finish=True, is_exchange=True)
				return render(request, template_name, locals())
			for getPart in completeBook.ebook_set.all():
				print 'get part'+getPart.__unicode__()
				getPart.editor = request.user.editor
				getPart.get_date = timezone.now()
				getPart.deadline = getPart.get_date + datetime.timedelta(days=3)
				getPart.save()
		elif request.POST.has_key('rebackPart'):
			book_ISBN = request.POST.get('rebackPart').split('-')[0]
#			book_ISBN = request.POST.keys()[request.POST.values().index(u'還文件')].split('-')[0]
			part_part = request.POST.get('rebackPart').split('-')[1]
#			part_part = request.POST.keys()[request.POST.values().index(u'還文件')].split('-')[1]
			rebackPart=EBook.objects.get(part=part_part, book__ISBN = book_ISBN)
			print 'reback'+rebackPart.__unicode__()
			rebackPart.editor=None
			rebackPart.get_date = None
			rebackPart.deadline = None
			rebackPart.save()
		elif request.POST.has_key('delay'):
			book_ISBN = request.POST.get('delay').split('-')[0]
			part_part = request.POST.get('delay').split('-')[1]
			delayPart = EBook.objects.get(part=part_part, book__ISBN = book_ISBN)
			delayPart.deadline = delayPart.deadline + datetime.timedelta(days=2)
			delayPart.save()
		elif request.POST.has_key('reEditPart'):
			book_ISBN = request.POST.get('reEditPart').split('-')[0]
			part_part = request.POST.get('reEditPart').split('-')[1]
			reEditPart = EBook.objects.get(part=part_part, book__ISBN = book_ISBN)
			reEditPart.is_finish = False
			reEditPart.save()
		elif request.POST.has_key('exchange'):
			book_ISBN = request.POST.get('exchange').split('-')[0]
			part_part = request.POST.get('exchange').split('-')[1]
			exchangePart = EBook.objects.get(part=part_part, book__ISBN = book_ISBN)
			exchangePart.is_exchange = True
			exchangePart.save()
		editingPartList=EBook.objects.filter(editor=user.editor, is_finish=False)
		finishPartList=EBook.objects.filter(editor=user.editor,is_finish=True)
		exchangedPartList=EBook.objects.filter(editor=user.editor,is_finish=True, is_exchange=True)
		return render(request, template_name, locals())