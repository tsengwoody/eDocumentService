from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^profile/$', views.profileView.as_view(template_name='guest/profile.html'), name='profile'),
]