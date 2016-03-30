from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^profile/$', views.profileView.as_view(template_name='guest/profile.html'), name='profile'),
	url(r'^book_save_test/$', views.book_save_test, name='book_save_test'),
	url(r'^create_document/$', views.create_document, name='create_document'),
	url(r'^upload/$', views.upload, name='upload'),
]