# coding: utf-8
from django import forms
from ebookSystem.models import *
from .models import *

class BookInfoForm(forms.ModelForm):
	class Meta:
		model = BookInfo
		fields = '__all__'

class ContactUsForm(forms.ModelForm):
	class Meta:
		model = ContactUs
		exclude = ['message_datetime']