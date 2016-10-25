# coding: utf-8
from django import forms
from ebookSystem.models import *
from .models import *

class BookInfoForm(forms.ModelForm):
	class Meta:
		model = BookInfo
		fields = '__all__'

'''class ContactUsForm(forms.ModelForm):
	class Meta:
		model = ContactUs
		exclude = ['datetime']'''

class UserChangeForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'first_name', 'last_name', 'phone', 'birthday', 'education']