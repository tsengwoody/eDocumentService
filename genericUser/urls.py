from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^(?P<template_name>\w+)/readme/$', views.readme, name='readme'),
	url(r'^contact_us/$', views.contact_us, {'template_name': 'genericUser/contact_us.html'}, name='contact_us'),
	url(r'^info/$', views.info, {'template_name': 'genericUser/info.html'}, name='info'),
	url(r'^info_change/$', views.info_change, {'template_name': 'genericUser/info_change.html'}, name='info_change'),
	url(r'^set_role/$', views.set_role, {'template_name': 'genericUser/set_role.html'}, name='set_role'),
	url(r'^review_user/(?P<username>[\w-]+)/$', views.review_user, name='review_user'),
	url(r'^test_message/$', views.test_message, {'template_name': 'genericUser/test_message.html'}, name='test_message'),
]
