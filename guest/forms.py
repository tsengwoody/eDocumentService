# coding: utf-8
from django import forms
from ebookSystem.models import Book
from .models import *

class BookForm(forms.ModelForm):
	fileObject = forms.FileField()
	class Meta:
		model = Book
		fields = ['bookname', 'author', 'translator', 'house', 'date', 'ISBN']

class UploadForm(forms.ModelForm):
	fileObject = forms.FileField()
	class Meta:
		model = Book
		fields = ['bookname', 'author', 'translator', 'house', 'date', 'ISBN']

class UploadFileForm(forms.ModelForm):
	class Meta:
		model = UploadFile
		fields = '__all__'