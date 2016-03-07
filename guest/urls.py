from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^create_document/$', views.create_document, name='create_document'),
]