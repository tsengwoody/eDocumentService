# coding: utf-8
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.views import login as auth_login
from django.contrib.auth import (REDIRECT_FIELD_NAME)
from django.contrib.auth.forms import (
    AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm,
)
from django.views import generic
from ebookSystem.models import *
from ebookSystem.forms import *

def info(request,template_name='account/info.html'):
	user = request.user
	return render(request, template_name, locals())

def info_change(request,template_name='account/info_change.html'):
	user = request.user
	if request.method == 'POST':
		editorform = EditorForm(request.POST, instance = user)
		editorform.save()
		redirect_to = '/account/info'
		return HttpResponseRedirect(redirect_to)
	if request.method == 'GET':
		editorform = EditorForm(instance = user)
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

def profile(request,template_name='account/profile.html'):
	user=request.user
#	finishPart=EBook.objects.filter(editor__username=user.username,is_finish=True)
#	editingPart=EBook.objects.filter(editor__username=user.username,is_finish=False)
	return render(request, template_name, locals())

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
			getPart = EBook.objects.filter(is_finish=False, editor=None).order_by('scan_date', 'part')[0]
			getPart.editor = request.user.editor
			getPart.save()
		elif u'還文件' in request.POST.values():
			print request.POST.keys()
			book_ISBN = request.POST.keys()[request.POST.values().index(u'還文件')].split('-')[0]
			part_part = request.POST.keys()[request.POST.values().index(u'還文件')].split('-')[1]
			rebackPart=EBook.objects.get(part=part_part, book__ISBN = book_ISBN)
			print rebackPart
			rebackPart.editor=None
			rebackPart.save()
		editingPartList=EBook.objects.filter(editor=user.editor, is_finish=False)
		finishPartList=EBook.objects.filter(editor=user.editor,is_finish=True)
		return render(request, template_name, locals())