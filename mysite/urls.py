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
from django.contrib.sitemaps import GenericSitemap
from django.contrib.sitemaps.views import sitemap

urlpatterns = [
#    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    url(r'^admin/', include(admin.site.urls)),
	url(r'^account/', include('account.urls', namespace="account", app_name="account")),
	url(r'^ebookSystem/', include('ebookSystem.urls', namespace="ebookSystem")),
	url(r'^genericUser/', include('genericUser.urls', namespace="genericUser")),
	url(r'^manager/', include('manager.urls', namespace="manager")),
	url(r'^guest/', include('guest.urls', namespace="guest")),
	url(r'^auth/password_change/$', auth_views.password_change, name='password_change'),
	url(r'^auth/register/$', views.register, name='register'),
	url(r'^auth/login/$', views.login_user, name='login'),
	url(r'^auth/logout/$', views.logout_user, name='logout'),
	url(r'^auth/', include('django.contrib.auth.urls',)),
	url(r'^locale/$', views.view_locale),
]
