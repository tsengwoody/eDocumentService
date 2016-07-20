# coding: utf-8
from django import forms
from genericUser.models import User
from snowpenguin.django.recaptcha2.fields import ReCaptchaField
from snowpenguin.django.recaptcha2.widgets import ReCaptchaWidget
from django.conf import settings
import requests


class RegisterUserForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['username', 'password', 'email', 'first_name', 'last_name', 'phone', 'birthday', 'education']


class FormWithCaptcha(forms.Form):
    captcha = ReCaptchaField(required=True,widget=ReCaptchaWidget())