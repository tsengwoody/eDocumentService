from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^mathml', views.mathml, name='mathml'),
	url(r'^tinymce_demo', views.tinymce_demo, name='tinymce_demo'),
	url(r'^get_resource', views.get_resource, name='get_resource'),
	url(r'^advanced/edit_(?P<type>\w+)/(?P<id>[0-9\-]+)/$', views.edit_SpecialContent, name='edit_SpecialContent'),
	url(r'^analyze_part/(?P<ISBN_part>[\d-]+)/$', views.analyze_part, name='analyze_part'),
	url(r'^book_info/(?P<ISBN>[0-9Xx]+)/$', views.book_info, name='book_info'),
	url(r'^book_list/$', views.book_list, name='book_list'),
	url(r'^book_list_manager/$', views.book_list_manager, name='book_list_manager'),
	url(r'^special_content/(?P<ISBN_part>[\d-]+)/$', views.special_content, name='special_content'),
	url(r'^detail/(?P<book_ISBN>[0-9]+)/$', views.detail, name='detail'),
	url(r'^detail_manager/(?P<book_ISBN>[0-9]+)/$', views.detail_manager, name='detail_manager'),
	url(r'^edit/(?P<ISBN_part>[0-9\-]+)/$', views.edit, name='edit'),
	url(r'^edit_ajax/(?P<ISBN_part>[0-9\-]+)/$', views.edit_ajax, name='edit_ajax'),
	url(r'^edit_log/(?P<ISBN_part>[\d-]+)/$', views.edit_log, name='edit_log'),
	url(r'^full_edit/(?P<ISBN_part>[0-9\-]+)/$', views.full_edit, name='full_edit'),
	url(r'^review_document/(?P<book_ISBN>[0-9]+)/$', views.review_document, name='review_document'),
	url(r'^review_part/(?P<ISBN_part>[\d-]+)/$', views.review_part, name='review_part'),
	url(r'^review_ApplyDocumentAction/(?P<id>[\d-]+)/$', views.review_ApplyDocumentAction, name='review_ApplyDocumentAction'),
	url(r'^review_ReviseContentAction/(?P<id>[\d-]+)/$', views.review_ReviseContentAction, name='review_ReviseContentAction'),
	url(r'^search_book/$', views.search_book, {'template_name':'ebookSystem/search_book.html'}, name='search_book'),
]