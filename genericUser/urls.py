from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^contact_us/$', views.contact_us, {'template_name': 'genericUser/contact_us.html'}, name='contact_us'),
]
