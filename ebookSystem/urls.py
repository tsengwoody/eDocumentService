from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^book_list/$', views.book_list.as_view(), name='book_list'),
	url(r'^detail/(?P<book_id>[0-9]+)/$', views.detail, name='detail'),
	url(r'^edit/(?P<book_id>[0-9]+)/(?P<part_id>[0-9]+)/$', views.editView.as_view(), name='edit'),
	url(r'^viewSource/(?P<book_id>[0-9]+)/(?P<page>[A-Za-z0-9._]+)/$', views.viewSource, name='viewSource'),
]