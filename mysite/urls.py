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
from django.contrib.auth import views as auth_views
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
def epub(request, ISBN, token, document_root=None, show_indexes=False):
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
#============

urlpatterns = [
	url(r'^$', views.home, name='home'),
	url(r'^about/(?P<name>[\w]+)$', views.about, name='about'),
	url(r'^sitemap$', views.sitemap, name='sitemap'),
	url(r'^error_social_auth$', views.error_social_auth, name='error_social_auth'),
	url(r'^epub/(?P<ISBN>[0-9]{13,13})/(?P<token>[abcdef0-9]{32,32})/$', epub),
	url(r'^admin/', include(admin.site.urls)),
	url(r'social-auth/', include('social_django.urls', namespace='social')),
	url(r'^account/', include('account.urls', namespace="account", app_name="account")),
	url(r'^ebookSystem/', include('ebookSystem.urls', namespace="ebookSystem")),
	url(r'^genericUser/', include('genericUser.urls', namespace="genericUser")),
	url(r'^manager/', include('manager.urls', namespace="manager")),
	url(r'^guest/', include('guest.urls', namespace="guest")),
	url(r'^auth/password_change/$', views.password_change, name='password_change'),
	url(r'^auth/register/$', views.register, name='register'),
	url(r'^auth/login/$', views.login, name='login'),
	url(r'^auth/logout/$', views.logout_user, name='logout'),
#	url(r'^auth/', include('django.contrib.auth.urls',)),
]
