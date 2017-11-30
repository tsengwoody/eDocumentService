from django.conf.urls import include, url

from . import views
from . import apis

book_list = apis.BookViewSet.as_view({
	'get': 'list',
})
book_detail = apis.BookViewSet.as_view({
	'get': 'retrieve',
})

ebook_list = apis.EBookViewSet.as_view({
	'get': 'list',
#	'post': 'create',
})
ebook_detail = apis.EBookViewSet.as_view({
	'get': 'retrieve',
#	'put': 'update',
#	'patch': 'partial_update',
#	'delete': 'destroy',
})

bookinfo_list = apis.BookInfoViewSet.as_view({
	'get': 'list',
})
bookinfo_detail = apis.BookInfoViewSet.as_view({
	'get': 'retrieve',
})

from rest_framework.routers import DefaultRouter
router = DefaultRouter()

import copy
api_urlpatterns = copy.copy(router.urls)
api_urlpatterns = api_urlpatterns +[
	url(r'^books/$', book_list, name='book-list'),
	url(r'^books/(?P<pk>[\d-]+)/$', book_detail, name='book-detail'),
	url(r'^ebooks/$', ebook_list, name='ebook-list'),
	url(r'^ebooks/(?P<pk>[\d-]+)/$', ebook_detail, name='ebook-detail'),
	url(r'^bookinfos/$', bookinfo_list, name='bookinfo-list'),
	url(r'^bookinfos/(?P<pk>[\d]+)/$', bookinfo_detail, name='bookinfo-detail'),
]

resource_urlpatterns = [
	url(r'^ebooks/(?P<pk>[\d-]+)/(?P<dir>[\w]+)/(?P<resource>[\d\w]+)/$', views.ebook_resource, name='ebook_resource'),
]

urlpatterns = [
	url(r'^mathml', views.mathml, name='mathml'),
	url(r'^tinymce_demo', views.tinymce_demo, name='tinymce_demo'),
	url(r'^analyze_part/(?P<ISBN_part>[\d-]+)/$', views.analyze_part, name='analyze_part'),
	url(r'^book_info/(?P<ISBN>[0-9Xx]+)/$', views.book_info, name='book_info'),
	url(r'^get_book_info_list/$', views.get_book_info_list, name='get_book_info_list'),
	url(r'^book_list_manager/$', views.book_list_manager, name='book_list_manager'),
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
	url(r'^book_list$', views.book_list, name='book_list'),
	url(r'^book_repository$', views.book_repository, name='book_repository'),
	url(r'^getbookrecord_user/(?P<ID>\d+)/$', views.getbookrecord_user, name='getbookrecord_user'),
	url(r'^library_view$', views.library_view, name='library_view'),
	url(r'^library_origin_view$', views.library_origin_view, name='library_origin_view'),
	url(r'^library_action$', views.library_action, name='library_action'),
	url(r'^book_saelf$', views.book_saelf, name='book_saelf'),
	url(r'^service/$', views.service, name='service'),
	url(r'^bookorder_list$', views.bookorder_list, name='bookorder_list'),
	url(r'^book_repository_person$', views.book_repository_person, name='book_repository_person'),
	url(r'^book_action/$', views.book_action, name='book_action'),
	url(r'^api/', include(api_urlpatterns, namespace='api')),
	url(r'^resource/', include(resource_urlpatterns, namespace='api')),
]