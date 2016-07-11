from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^review_user_list/$', views.review_user_list, name='review_user_list'),
	url(r'^review_document_list/$', views.review_document_list, name='review_document_list'),
	url(r'^review_part_list/$', views.review_part_list, name='review_part_list'),
	url(r'^event_list/(?P<action>\w+)/$', views.event_list, name='event_list'),
]
