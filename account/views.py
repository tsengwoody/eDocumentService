# coding: utf-8
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.views import login as auth_login
from django.contrib.auth import (REDIRECT_FIELD_NAME)
from django.contrib.auth.forms import (
    AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm,
)
from django.db.models import F
from django.views import generic
from ebookSystem.models import *
from ebookSystem.forms import *

def info(request,template_name='account/info.html'):
	user = request.user
	return render(request, template_name, locals())

def info_change(request,template_name='account/info_change.html'):
	user = request.user
	if request.method == 'POST':
		registerUserForm = registerUserForm(request.POST, instance = user)
		registerUserForm.save()
		redirect_to = '/account/info'
		return HttpResponseRedirect(redirect_to)
	if request.method == 'GET':
		registerUserForm = RegisterUserForm(instance = user)
		return render(request, template_name, locals())

def login(request, template_name='registration/login.html',
		redirect_field_name=REDIRECT_FIELD_NAME,
		authentication_form=AuthenticationForm,
		current_app=None, extra_context=None):
	if request.user.is_authenticated():
		redirect_to = '/accounts/profile'
		return HttpResponseRedirect(redirect_to)
	else:
		return auth_login(request, template_name, redirect_field_name, authentication_form, current_app)

class profileView(generic.View):
	template_name=''
	def get(self, request, *args, **kwargs):
		template_name=self.template_name
		if request.user.is_authenticated():
			user=request.user
			editingPartList=EBook.objects.filter(editor=user.editor, is_finish=False)
			finishPartList=EBook.objects.filter(editor=user.editor,is_finish=True)
		return render(request, template_name, locals())

	def post(self, request, *args, **kwargs):
		template_name='account/profile.html'
		user=request.user
		if request.POST.has_key('getPart'):
			try:
				partialBook = Book.objects.exclude(get_count=0).exclude(get_count = F('part_count')).order_by('get_count')[0]
			except IndexError:
				print 'not partial book'
				try:
					partialBook = Book.objects.filter(get_count=0).order_by('upload_date')[0]
				except IndexError:
					error_message = u'無文件'
					print 'not book'
					editingPartList=EBook.objects.filter(editor=user.editor, is_finish=False)
					finishPartList=EBook.objects.filter(editor=user.editor,is_finish=True)
					return render(request, template_name, locals())
			getPart = partialBook.ebook_set.filter(is_finish=False, editor=None)[0]
			print 'get part'+getPart.__unicode__()
			getPart.editor = request.user.editor
			getPart.book.get_count = getPart.book.get_count+1
			getPart.save()
			getPart.book.save()
		elif request.POST.has_key('getCompleteBook'):
			try:
				completeBook = Book.objects.filter(get_count=0).order_by('upload_date')[0]
			except IndexError:
				error_message = u'目前無完整書文件，請先領部份文件'
				print 'not Complete book'
				editingPartList=EBook.objects.filter(editor=user.editor, is_finish=False)
				finishPartList=EBook.objects.filter(editor=user.editor,is_finish=True)
				return render(request, template_name, locals())
			for getPart in completeBook.ebook_set.all():
				print 'get part'+getPart.__unicode__()
				getPart.editor = request.user.editor
				getPart.book.get_count = getPart.book.get_count+1
				getPart.save()
				getPart.book.save()
		elif u'還文件' in request.POST.values():
			book_ISBN = request.POST.keys()[request.POST.values().index(u'還文件')].split('-')[0]
			part_part = request.POST.keys()[request.POST.values().index(u'還文件')].split('-')[1]
			rebackPart=EBook.objects.get(part=part_part, book__ISBN = book_ISBN)
			print 'reback'+rebackPart.__unicode__()
			rebackPart.editor=None
			rebackPart.book.get_count = rebackPart.book.get_count-1
			rebackPart.save()
			rebackPart.book.save()
		editingPartList=EBook.objects.filter(editor=user.editor, is_finish=False)
		finishPartList=EBook.objects.filter(editor=user.editor,is_finish=True)
		return render(request, template_name, locals())