# coding: utf-8
from django import forms
from ebookSystem.models import *
from .models import *

EDUCATION_OPTION = (
	(u'國小' , u'國小'),
	(u'國中' , u'國中'),
	(u'高中' , u'高中'),
	(u'學士' , u'學士'),
	(u'碩士' , u'碩士'),
)

EMPTY_OPTION = (('', u'---------'),)

class UserForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'first_name', 'last_name', 'phone', 'birthday', 'education', 'is_book', 'org',]
		widgets = {
			'username': forms.TextInput(
				attrs={
					'autofocus': True,
					'required': True,
					'pattern': "^[a-z][a-z0-9_]*$",
					'placeholder': 'username',
				},
			),
			'email': forms.EmailInput(
				attrs={
					'required': True,
					'placeholder': 'Email',
				},
			),
			'first_name': forms.TextInput(
				attrs={
					'required': True,
					'placeholder': 'first name',
				},
			),
			'last_name': forms.TextInput(
				attrs={
					'required': True,
					'placeholder': 'last name',
				},
			),
			'phone': forms.TextInput(
				attrs={
					'required': True,
					'pattern': '^[0-9]{10}$',
					'placeholder': 'phone',
				},
			),
			'birthday': forms.TextInput(
				attrs={
					'class': 'datepicker',
					'required': True,
					'pattern': '^[0-9]{4}-[0-9]{2}-[0-9]{2}$',
					'placeholder': 'birthday',
				},
			),
			'education': forms.Select(
				attrs={
					'required': True,
				},
				choices = EMPTY_OPTION +EDUCATION_OPTION,
			),
		}
		labels = {
			'username': u'使用者名稱',
			'email': u'電子信箱',
			'first_name': u'姓氏',
			'last_name': u'名字',
			'phone': u'聯絡電話',
			'birthday': u'生日',
			'education': u'教育程度',
			'is_book': u'訂閱訊息',
			'org': u'所屬單位',
		}
		help_texts = {
			'username': u'請使用小寫英文字母或數字，首字必需為小寫英文字母',
			'email': u'請填寫電子信箱',
			'first_name': u'請填寫中文姓名',
			'last_name': u'請填寫中文姓名',
			'phone': u'請填寫手機',
			'birthday': u'範例日期格式：1989-02-19',
			'education': u'請選擇教育程度',
			'is_book': u'訂閱訊息',
			'org': u'請選擇所屬單位',
		}

	def __init__(self, *args, **kwargs):
		kwargs.setdefault('label_suffix', '')
		super(UserForm, self).__init__(*args, **kwargs)
		field_order = ['username', 'first_name', 'last_name', 'email', 'phone', 'birthday', 'education', 'is_book', 'org',]
		self.fields = type(self.fields)((k, self.fields[k]) for k in field_order)
		self.fields['org'].empty_label = u'其他'
		try:
			field_cannot_modify = []
			if kwargs['instance'].status is not kwargs['instance'].STATUS['review']:
				field_cannot_modify = field_cannot_modify +['username', 'first_name', 'last_name',]
			if kwargs['instance'].auth_phone == True:
				field_cannot_modify.append('phone')
			for field in self:
				if field.name in field_cannot_modify:
					field.can_modify = False
				else:
					field.can_modify = True
		except:
			pass

class RoleForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['is_active', 'is_editor', 'is_guest', 'auth_email', 'auth_phone']

class InfoAuthForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'first_name', 'last_name', 'phone', 'birthday', 'education', 'is_book', 'org', 'auth_email', 'auth_phone',]
