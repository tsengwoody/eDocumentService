from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^contact_us/$', views.contact_us, {'template_name': 'genericUser/contact_us.html'}, name='contact_us'),
	url(r'^info/$', views.info, {'template_name': 'genericUser/info.html'}, name='info'),
	url(r'^info/info_change/$', views.info_change, {'template_name': 'genericUser/info_change.html'}, name='info_change'),
]
