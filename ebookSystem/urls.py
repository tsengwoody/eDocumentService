from django.conf.urls import include, url

from . import views
from . import apis

from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'books', apis.BookViewSet)
router.register(r'bookadds', apis.BookAddViewSet)
router.register(r'ebooks', apis.EBookViewSet)
router.register(r'bookinfos', apis.BookInfoViewSet)
router.register(r'editrecords', apis.EditRecordViewSet)
router.register(r'issnbookinfos', apis.ISSNBookInfoViewSet)
router.register(r'issnbooks', apis.ISSNBookViewSet)
router.register(r'bookrecommends', apis.BookRecommendViewSet)
router.register(r'libraryrecords', apis.LibraryRecordViewSet)
router.register(r'bookorders', apis.BookOrderViewSet)

import copy
api_urlpatterns = copy.copy(router.urls)

urlpatterns = [
	url(r'^mathml', views.mathml, name='mathml'),
	url(r'^book_info/(?P<ISBN>[0-9Xx]+)/$', views.book_info, name='book_info'),
	url(r'^get_book_info_list/$', views.get_book_info_list, name='get_book_info_list'),
	url(r'^edit/(?P<ISBN_part>[0-9\-]+)/$', views.edit, name='edit'),
	url(r'^edit_ajax/(?P<ISBN_part>[0-9\-]+)/$', views.edit_ajax, name='edit_ajax'),
	url(r'^review_document/(?P<book_ISBN>[0-9]+)/$', views.review_document, name='review_document'),
	url(r'^message_send$', views.message_send, name='message_send'),
	url(r'^book_delete/$', views.book_delete, name='book_delete'),
	url(r'^library_view$', views.library_view, name='library_view'),
	url(r'^library_origin_view$', views.library_origin_view, name='library_origin_view'),
	url(r'^library_action$', views.library_action, name='library_action'),
	url(r'^bookorder_list$', views.bookorder_list, name='bookorder_list'),
	url(r'^book_action/$', views.book_action, name='book_action'),
	url(r'^ebook_change_status/(?P<pk>[\d-]+)/$', views.ebook_change_status, name='ebook_change_status'),
	url(r'^api/', include(api_urlpatterns, namespace='api')),
	url(r'^generics/(?P<name>[\w\d/_\-]+)/$', views.generics, name='generics'),
]