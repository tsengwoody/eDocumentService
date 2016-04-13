from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^(?P<template_name>\w+)/readme/$', views.readme, name='readme'),
	url(r'^profile/$', views.profileView.as_view(template_name='guest/profile.html'), name='profile'),
	url(r'^create_document/$', views.create_document, name='create_document'),
	url(r'^upload_progress/$', views.upload_progress, name='upload_progress'),
]