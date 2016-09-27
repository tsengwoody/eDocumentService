from django.conf.urls import url

from . import views

urlpatterns = [
#	url(r'^advanced/edit_image/(?P<id>[0-9\-]+)/$', views.edit_image, name='edit_image'),
#	url(r'^advanced/edit_mathml/(?P<id>[0-9\-]+)/$', views.edit_mathml, name='edit_mathml'),
#	url(r'^advanced/edit_unknown/(?P<id>[0-9\-]+)/$', views.edit_unknown, name='edit_unknown'),
	url(r'^mathml', views.mathml, name='mathml'),
	url(r'^advanced/edit_(?P<type>\w+)/(?P<id>[0-9\-]+)/$', views.edit_SpecialContent, name='edit_SpecialContent'),
	url(r'^book_info/(?P<ISBN>[0-9Xx]+)/$', views.book_info, name='book_info'),
	url(r'^book_list/$', views.book_list.as_view(), name='book_list'),
	url(r'^special_content/(?P<ISBN_part>[\d-]+)/$', views.special_content, name='special_content'),
	url(r'^detail/(?P<book_ISBN>[0-9]+)/$', views.detail, name='detail'),
	url(r'^edit/(?P<ISBN_part>[0-9\-]+)/$', views.editView.as_view(), name='edit'),
	url(r'^edit_ajax/(?P<ISBN_part>[0-9\-]+)/$', views.edit_ajax, name='edit_ajax'),
	url(r'^review_document/(?P<book_ISBN>[0-9]+)/$', views.review_document, name='review_document'),
	url(r'^review_part/(?P<ISBN_part>[\d-]+)/$', views.review_part, name='review_part'),
	url(r'^review_ApplyDocumentAction/(?P<id>[\d-]+)/$', views.review_ApplyDocumentAction, name='review_ApplyDocumentAction'),
	url(r'^review_ReviseContentAction/(?P<id>[\d-]+)/$', views.review_ReviseContentAction, name='review_ReviseContentAction'),
	url(r'^search_book/$', views.search_book, {'template_name':'ebookSystem/search_book.html'}, name='search_book'),
]