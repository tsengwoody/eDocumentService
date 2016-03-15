# coding: utf-8
from django import forms

class UploadForm(forms.Form):
	path = forms.CharField()
	fileObject = forms.FileField()