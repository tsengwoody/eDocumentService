# coding: utf-8
from django import forms

class UploadForm(forms.Form):
	filename = forms.CharField()
	fileObject = forms.FileField()