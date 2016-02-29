# coding: utf-8
from django import forms

class EditForm(forms.Form):
	content = forms.CharField(widget=forms.Textarea(attrs={'rows': 200, 'cols':60}), label=u'內容')
	page = forms.IntegerField(label=u'頁數')

#	def clean_content(self):
#		data = self.cleaned_data['content']
#		if data.find('|----------|') == -1:
#			raise forms.ValidationError("無法儲存檔案，您傳的資料無特殊標記無法得知校對完成位置")
#		return data

class EditorForm(ModelForm):
	class Meta:
		model = User
		fields = ['email', 'first_name', 'last_name']