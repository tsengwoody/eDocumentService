# coding: utf-8
from django import forms
from ebookSystem.models import *
from .models import *

'''class BookForm(forms.ModelForm):
	fileObject = forms.FileField()
	class Meta:
		model = Book
		fields = ['bookname', 'author', 'house', 'date', 'ISBN']'''

class BookInfoForm(forms.ModelForm):
	class Meta:
		model = BookInfo
		fields = '__all__'

class InfoChangeUserForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['email', 'phone']

class ContactUsForm(forms.ModelForm):
	class Meta:
		model = ContactUs
		exclude = ['message_datetime']