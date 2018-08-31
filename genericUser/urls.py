from django.conf.urls import include, url

from . import views
from . import apis
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'announcements', apis.AnnouncementViewSet)
router.register(r'organizations', apis.OrganizationViewSet)
router.register(r'businesscontents', apis.BusinessContentViewSet)
router.register(r'qandas', apis.QAndAViewSet)
router.register(r'bannercontents', apis.BannerContentViewSet)
router.register(r'serviceinfos', apis.ServiceInfoViewSet)
router.register(r'users', apis.UserViewSet)
router.register(r'disabilitycards', apis.DisabilityCardViewSet)

import copy
api_urlpatterns = copy.copy(router.urls)

import rest_framework

urlpatterns = [
	url(r'^user_guide', views.user_guide, name='user_guide'),
	url(r'^recruit', views.recruit, name='recruit'),
	url(r'^func_desc/$', views.func_desc, name='func_desc'),
	url(r'^org_info$', views.org_info, name='org_info'),
	url(r'^upload_progress/$', views.upload_progress, name='upload_progress'),
	url(r'^event_list/$', views.event_list, name='event_list'),
	url(r'^retrieve_password/$', views.retrieve_password, name='retrieve_password'),
	url(r'^review_user/(?P<username>[\w-]+)/$', views.review_user, name='review_user'),
	url(r'^generics/(?P<name>[\w\d/_\-]+)/$', views.generics, name='generics'),
	url(r'^api/', include(api_urlpatterns, namespace='api')),
	url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
