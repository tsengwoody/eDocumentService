# coding: utf-8
from django import forms
from ebookSystem.models import *
from genericUser.models import *
from guest.models import *
from .models import *

class InfoChangeUserForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['first_name', 'last_name', 'email', 'phone', 'birthday']

class BookForm(forms.ModelForm):
	class Meta:
		model = Book
		fields = ['bookname', 'author', 'translator', 'house', 'date', 'ISBN']

class ContactUsForm(forms.ModelForm):
	class Meta:
		model = ContactUs
		exclude = ['message_datetime']