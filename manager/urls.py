from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^event_list/(?P<action>\w+)/$', views.event_list, name='event_list'),
]
