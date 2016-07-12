# coding: utf-8
from django import forms
from ebookSystem.models import Book
from .models import *

class UploadFileForm(forms.ModelForm):
	class Meta:
		model = UploadFile
		fields = '__all__'