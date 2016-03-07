# coding: utf-8
from django import forms
from .models import *

class EditForm(forms.Form):
	content = forms.CharField()
	page = forms.IntegerField()

#	def clean_content(self):
#		data = self.cleaned_data['content']
#		if data.find('|----------|') == -1:
#			raise forms.ValidationError("無法儲存檔案，您傳的資料無特殊標記無法得知校對完成位置")
#		return data

class RegisterUserForm(forms.ModelForm):
	class Meta:
		model = User
		fields = '__all__'

class BookForm(forms.ModelForm):
	class Meta:
		model = Book
		fields = '__all__'

class ContactUsForm(forms.ModelForm):
	class Meta:
		model = ContactUs
		fields = '__all__'