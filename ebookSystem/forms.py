# coding: utf-8
from django import forms
from .models import *

class BookInfoForm(forms.ModelForm):
	class Meta:
		model = BookInfo
		fields = '__all__'

	'''def save(self, *args, **kwargs):
		try:
			commit = kwargs['commit']
		except:
			commit = True
		kwargs['commit'] = False
		instance = super(BookInfoForm, self).save(*args, **kwargs)
		if commit:
			try:
				newBookInfo = BookInfo.objects.get(ISBN=self.data['ISBN'])
				print 'YA'
			except:
				instance.save()
				print 'YA2'
		return instance'''

class EditForm(forms.Form):
	content = forms.CharField()
	page = forms.IntegerField()
