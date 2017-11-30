from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^an_service/$', views.an_service, name='an_service'),
	url(r'^sc_service/$', views.sc_service, name='sc_service'),
]
