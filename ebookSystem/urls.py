from django.urls import path
from django.conf.urls import include, url

from . import views
from . import apis

from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'booksimples', apis.BookSimpleViewSet)
router.register(r'books', apis.BookViewSet)
router.register(r'bookadds', apis.BookAddViewSet)
router.register(r'ebooks', apis.EBookViewSet)
router.register(r'bookinfos', apis.BookInfoViewSet)
router.register(r'editrecords', apis.EditRecordViewSet)
router.register(r'issnbookinfos', apis.ISSNBookInfoViewSet)
router.register(r'issnbooks', apis.ISSNBookViewSet)
router.register(r'libraryrecords', apis.LibraryRecordViewSet)
router.register(r'categorys', apis.CategoryViewSet)
router.register(r'bookorders', apis.BookOrderViewSet)

urlpatterns = [
	url(r'^library_view$', views.library_view, name='library_view'),
	url(r'^library_origin_view$', views.library_origin_view, name='library_origin_view'),
	url(r'^generics/(?P<name>[\w\d/_\-]+)/$', views.generics, name='generics'),
	path('api/', include((router.urls, 'ebookSystem'), 'api'),)
]