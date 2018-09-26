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
	url(r'^edit/(?P<ISBN_part>[0-9\-]+)/$', views.edit, name='edit'),
	url(r'^edit_ajax/(?P<ISBN_part>[0-9\-]+)/$', views.edit_ajax, name='edit_ajax'),
	url(r'^library_view$', views.library_view, name='library_view'),
	url(r'^library_origin_view$', views.library_origin_view, name='library_origin_view'),
	url(r'^book_action/$', views.book_action, name='book_action'),
	url(r'^api/', include(api_urlpatterns, namespace='api')),
	url(r'^generics/(?P<name>[\w\d/_\-]+)/$', views.generics, name='generics'),
]