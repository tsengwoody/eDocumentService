# coding: utf-8
from django.shortcuts import render

# Create your views here.

from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse
from ebookSystem.models import *
from ebookSystem.forms import *

def create_document(request, template_name='guest/create_document.html'):
	bookForm = BookForm()
	return render(request, template_name, locals())