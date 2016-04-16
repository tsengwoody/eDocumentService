from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^(?P<template_name>\w+)/readme/$', views.readme, name='readme'),
	url(r'^review/$', views.review, name='review'),
	url(r'^(?P<template_name>\w+)/$', views.static, name='static'),
]
