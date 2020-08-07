from django.urls import path
from django.conf.urls import include, url

from . import apis
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'announcements', apis.AnnouncementViewSet)
router.register(r'organizations', apis.OrganizationViewSet)
router.register(r'businesscontents', apis.BusinessContentViewSet)
router.register(r'qandas', apis.QAndAViewSet)
router.register(r'bannercontents', apis.BannerContentViewSet)
router.register(r'recommendationsubjects', apis.RecommendationSubjectViewSet)
router.register(r'serviceinfos', apis.ServiceInfoViewSet)
router.register(r'users', apis.UserViewSet)
router.register(r'disabilitycards', apis.DisabilityCardViewSet)

import copy
api_urlpatterns = copy.copy(router.urls)

import rest_framework

urlpatterns = [
	path('api/', include((router.urls, 'genericUser'), 'api'),)
]