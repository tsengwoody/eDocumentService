# coding: utf-8
from django import forms
from .models import *

class RegisterUserForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['username', 'password', 'email', 'phone', 'birthday']

class ContactUsForm(forms.ModelForm):
	class Meta:
		model = ContactUs
		exclude = ['message_datetime']