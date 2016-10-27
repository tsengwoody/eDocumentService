from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^book_repository/$', views.book_repository, name='book_repository'),
]