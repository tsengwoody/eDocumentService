from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from ebookSystem.models import *
from ebookSystem.forms import *

def register(request, template_name='registration/register.html'):
	if request.method == 'POST':
		registerUserForm = RegisterUserForm(request.POST)
		newUser = registerUserForm.save(commit=False)
		newUser.username = request.POST.get('username')
		newUser.set_password(request.POST.get('password'))
		newUser.is_active = False
		newUser.save()
		newEditor = Editor(user=newUser, service_hours=0)
		newEditor.save()
		redirect_to = '/auth/login/'
		return HttpResponseRedirect(redirect_to)
#		return render(request, template_name, locals())
	if request.method == 'GET':
		registerUserForm = RegisterUserForm()
		return render(request, template_name, locals())