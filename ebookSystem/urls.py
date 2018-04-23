from django.conf.urls import include, url

from . import views
from . import apis

from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'books', apis.BookViewSet)
router.register(r'ebooks', apis.EBookViewSet)
router.register(r'bookinfos', apis.BookInfoViewSet)
router.register(r'editrecords', apis.EditRecordViewSet)
router.register(r'issnbookinfos', apis.ISSNBookInfoViewSet)
router.register(r'issnbooks', apis.ISSNBookViewSet)

import copy
api_urlpatterns = copy.copy(router.urls)

urlpatterns = [
	url(r'^mathml', views.mathml, name='mathml'),
	url(r'^analyze_part/(?P<ISBN_part>[\d-]+)/$', views.analyze_part, name='analyze_part'),
	url(r'^book_info/(?P<ISBN>[0-9Xx]+)/$', views.book_info, name='book_info'),
	url(r'^get_book_info_list/$', views.get_book_info_list, name='get_book_info_list'),
	url(r'^detail/(?P<book_ISBN>[0-9]+)/$', views.detail, name='detail'),
	url(r'^detail_manager/(?P<book_ISBN>[0-9]+)/$', views.detail_manager, name='detail_manager'),
	url(r'^edit/(?P<ISBN_part>[0-9\-]+)/$', views.edit, name='edit'),
	url(r'^edit_ajax/(?P<ISBN_part>[0-9\-]+)/$', views.edit_ajax, name='edit_ajax'),
	url(r'^edit_log/(?P<ISBN_part>[\d-]+)/$', views.edit_log, name='edit_log'),
	url(r'^full_edit/(?P<ISBN_part>[0-9\-]+)/$', views.full_edit, name='full_edit'),
	url(r'^review_document/(?P<book_ISBN>[0-9]+)/$', views.review_document, name='review_document'),
	url(r'^review_part/(?P<ISBN_part>[\d-]+)/$', views.review_part, name='review_part'),
	url(r'^review_ApplyDocumentAction/(?P<id>[\d-]+)/$', views.review_ApplyDocumentAction, name='review_ApplyDocumentAction'),
	url(r'^book_download/(?P<ISBN>[0-9]+)$', views.book_download, name='book_download'),
	url(r'^ebook_download/(?P<ISBN_part>[0-9\-]+)$', views.ebook_download, name='ebook_download'),
	url(r'^message_send$', views.message_send, name='message_send'),
	url(r'^book_create/$', views.book_create, name='book_create'),
	url(r'^book_upload/$', views.book_upload, name='book_upload'),
	url(r'^book_delete/$', views.book_delete, name='book_delete'),
	url(r'^getbookrecord_user/(?P<ID>\d+)/$', views.getbookrecord_user, name='getbookrecord_user'),
	url(r'^library_view$', views.library_view, name='library_view'),
	url(r'^library_origin_view$', views.library_origin_view, name='library_origin_view'),
	url(r'^library_action$', views.library_action, name='library_action'),
	url(r'^book_saelf$', views.book_saelf, name='book_saelf'),
	url(r'^service/$', views.service, name='service'),
	url(r'^sc_service/$', views.sc_service, name='sc_service'),
	url(r'^bookorder_list$', views.bookorder_list, name='bookorder_list'),
	url(r'^book_action/$', views.book_action, name='book_action'),
	url(r'^ebook_change_status/(?P<pk>[\d-]+)/$', views.ebook_change_status, name='ebook_change_status'),
	url(r'^api/', include(api_urlpatterns, namespace='api')),
	url(r'^generics/(?P<name>[\w\d]+)/$', views.generics, name='generics'),
]