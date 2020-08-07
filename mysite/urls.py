"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
	https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
	1. Add an import:  from my_app import views
	2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
	1. Add an import:  from other_app.views import Home
	2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
	1. Import the include() function: from django.urls import include, path
	2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url

from . import apis
from . import views
from .settings import BASE_DIR
from django.views.static import serve

from rest_framework_simplejwt.views import (
	TokenObtainPairView,
	TokenRefreshView,
	TokenVerifyView,
)

urlpatterns = [
	url(r'^api/token/$', TokenObtainPairView.as_view(), name='token_obtain_pair'),
	url(r'^api/token/refresh/$', TokenRefreshView.as_view(), name='token_refresh'),
	url(r'^api/token/verify/$', TokenVerifyView.as_view(), name='token_verify'),
	path('ebookSystem/', include(('ebookSystem.urls','ebookSystem'), namespace='ebookSystem')),
	path('genericUser/', include(('genericUser.urls','genericUser'), namespace='genericUser')),
	path('admin/', admin.site.urls),
	url(r'^file/(?P<path>.*)$', serve, {'document_root': BASE_DIR +'/file/'}),
	url(r'^$', views.home, name='home'),
	url(r'^api/statistics/(?P<action>[\d\w]+)/$', apis.Statistics.as_view()),
	url(r'^routing/(?P<name>[\w\d/_\-]+)/$', views.routing, name='routing'),
	url(r'^api/ddm/(?P<action>[\d\w]+)/(?P<dir>[\d\w]+)/$', apis.Ddm.as_view()),
	url(r'^api/ddm/(?P<action>[\d\w]+)/(?P<dir>[\d\w]+)/(?P<resource>.+)/$', apis.Ddm.as_view()),
]

urlpatterns = urlpatterns +[
	url(r'^file/(?P<path>.*)$', serve, {'document_root': BASE_DIR +'/static/'}),
]

urlpatterns = urlpatterns +[
	url(r'^static/(?P<path>.*)$', serve, {'document_root': BASE_DIR +'/static/'}),
]