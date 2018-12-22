"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
	https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
	1. Add an import:  from my_app import views
	2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
	1. Add an import:  from other_app.views import Home
	2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
	1. Add an import:  from blog import urls as blog_urls
	2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from . import views
from .settings import BASE_DIR

#============
import mimetypes
import os
import stat

from django.http import (
	FileResponse, Http404, HttpResponse, HttpResponseNotModified,
	HttpResponseRedirect,
)

from django.core.cache import cache

def library_epub(request, ISBN, token, document_root=None, show_indexes=False):
	from ebookSystem.models import Book, LibraryRecord
	lr = LibraryRecord.objects.get(id=ISBN)
	fullpath = lr.epub

	if not os.path.exists(fullpath):
		raise Http404(_('"%(path)s" does not exist') % {'path': fullpath})
	# Respect the If-Modified-Since header.
	statobj = os.stat(fullpath)
	content_type, encoding = mimetypes.guess_type(fullpath)
	content_type = content_type or 'application/octet-stream'
	response = FileResponse(open(fullpath, 'rb'), content_type=content_type)
#	response["Last-Modified"] = http_date(statobj.st_mtime)
#	if stat.S_ISREG(statobj.st_mode):
#		response["Content-Length"] = statobj.st_size
	if encoding:
		response["Content-Encoding"] = encoding
#	if token == cache.get('token.' +str(request.user.id)):
	return response
#============

def library_origin_epub(request, ISBN, token, document_root=None, show_indexes=False):
	from ebookSystem.models import Book
	book = Book.objects.get(ISBN=ISBN)
	fullpath = book.path +'/OCR/{0}.epub'.format(book.ISBN)
	if not os.path.exists(fullpath):
		raise Http404(_('"%(path)s" does not exist') % {'path': fullpath})
	# Respect the If-Modified-Since header.
	statobj = os.stat(fullpath)
	content_type, encoding = mimetypes.guess_type(fullpath)
	content_type = content_type or 'application/octet-stream'
	response = FileResponse(open(fullpath, 'rb'), content_type=content_type)
#	response["Last-Modified"] = http_date(statobj.st_mtime)
#	if stat.S_ISREG(statobj.st_mode):
#		response["Content-Length"] = statobj.st_size
	if encoding:
		response["Content-Encoding"] = encoding
#	if token == cache.get('token.' +str(request.user.id)):
	return response
from . import apis
from django.views.static import serve

urlpatterns = [
	url(r'^file/(?P<path>.*)$', serve, {'document_root': BASE_DIR +'/file/'}),
	url(r'^$', views.home, name='home'),
	url(r'^dev/(?P<name>[\w\d/_\-]+)/$', views.dev, name='dev'),
	url(r'^about/(?P<name>[\w]+)/$', views.about, name='about'),
	url(r'^library_epub/(?P<ISBN>[0-9]+)/(?P<token>[abcdef0-9]{32,32})/$', library_epub),
	url(r'^library_origin_epub/(?P<ISBN>[0-9]+)/(?P<token>[abcdef0-9]{32,32})/$', library_origin_epub),
	url(r'^admin/', include(admin.site.urls)),
	url(r'^ebookSystem/', include('ebookSystem.urls', namespace="ebookSystem")),
	url(r'^genericUser/', include('genericUser.urls', namespace="genericUser")),
	url(r'^api/statistics/(?P<action>[\d\w]+)/$', apis.Statistics.as_view()),
	url(r'^auth/logout/$', views.logout_user, name='logout'),
	url(r'^statistics_old/$', views.statistics, name='statistics'),
	url(r'^generics/(?P<name>[\w\d/_\-]+)/$', views.generics, name='generics'),
	url(r'^routing/(?P<name>[\w\d/_\-]+)/$', views.routing, name='routing'),
	url(r'^epub_view/(?P<path>.+)/$', views.epub_view, name='epub_view'),
	url(r'^api/ddm/(?P<action>[\d\w]+)/(?P<dir>[\d\w]+)/$', apis.Ddm.as_view()),
	url(r'^api/ddm/(?P<action>[\d\w]+)/(?P<dir>[\d\w]+)/(?P<resource>.+)/$', apis.Ddm.as_view()),
]

from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token
urlpatterns = urlpatterns +[
	url(r'^api-token-auth/', obtain_jwt_token),
	url(r'^api-token-refresh/', refresh_jwt_token),
]
