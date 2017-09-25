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
from django.views.static import serve

urlpatterns = [
	url(r'^$', views.home, name='home'),
	url(r'^sitemap$', views.sitemap, name='sitemap'),
#	url(r'^file/(?P<path>.*)$', serve, {'document_root': 'file/'}),
	url(r'^admin/', include(admin.site.urls)),
	url(r'social-auth/', include('social_django.urls', namespace='social')),
	url(r'^social_auth_test$', views.social_auth_test, name='social-auth_test'),
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
