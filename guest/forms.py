# coding: utf-8
from django import forms
from ebookSystem.models import Book

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