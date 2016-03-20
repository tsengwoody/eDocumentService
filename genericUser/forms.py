# coding: utf-8
from django import forms
from .models import *

class RegisterUserForm(forms.ModelForm):
	class Meta:
		model = User
		fields = '__all__'

class ContactUsForm(forms.ModelForm):
	class Meta:
		model = ContactUs
		fields = '__all__'