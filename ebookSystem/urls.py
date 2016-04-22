from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^book_list/$', views.book_list.as_view(), name='book_list'),
	url(r'^detail/(?P<book_ISBN>[0-9]+)/$', views.detail, name='detail'),
	url(r'^edit/(?P<book_ISBN>[0-9]+)/(?P<part_part>[0-9]+)/$', views.editView.as_view(), name='edit'),
	url(r'^edit_ajax/(?P<book_ISBN>[0-9]+)/(?P<part_part>[0-9]+)/$', views.edit_ajax, name='edit_ajax'),
	url(r'^review_document/(?P<book_ISBN>[0-9]+)/$', views.review_document, name='review_document'),
	url(r'^review_part/(?P<ISBN_part>[\d-]+)/$', views.review_part, name='review_part'),
	url(r'^search_book/$', views.search_book, name='search_book'),
]