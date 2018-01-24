from django.conf.urls import include, url

from . import views
from . import apis

organization_list = apis.OrganizationViewSet.as_view({
	'get': 'list',
})

from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'announcements', apis.AnnouncementViewSet)
router.register(r'organizations', apis.OrganizationViewSet)
router.register(r'qandas', apis.QAndAViewSet)
router.register(r'serviceinfos', apis.ServiceInfoViewSet)
router.register(r'users', apis.UserViewSet)

import copy
api_urlpatterns = copy.copy(router.urls)

import rest_framework

resource_urlpatterns = [
	url(r'^users/(?P<pk>[\d-]+)/(?P<dir>[\w]+)/(?P<resource>[\d\w]+)/$', views.UserResource.as_view(), name='user-resource'),
]

urlpatterns = [
	url(r'^refactor/(?P<name>[\w-]+)/$', views.refactor, name='refactor'),
	url(r'^refactor/(?P<name>[\w-]+)/(?P<pk>[\d-]+)/$', views.refactor_detail, name='refactor-detail'),
	url(r'^user_guide', views.user_guide, name='user_guide'),
	url(r'^recruit', views.recruit, name='recruit'),
	url(r'^apply_document/$', views.apply_document, name='apply_document'),
	url(r'^func_desc/$', views.func_desc, name='func_desc'),
	url(r'^org_info$', views.org_info, name='org_info'),
	url(r'^license/$', views.license, name='license'),
	url(r'^upload_progress/$', views.upload_progress, name='upload_progress'),
	url(r'^event_list/$', views.event_list, name='event_list'),
	url(r'^serviceinfo_list/$', views.serviceinfo_list, name='serviceinfo_list'),
	url(r'^serviceinfo_list_check/$', views.serviceinfo_list_check, name='serviceinfo_list_check'),
	url(r'^info/$', views.info, {'template_name': 'genericUser/info.html'}, name='info'),
	url(r'^change_contact_info/$', views.change_contact_info, {'template_name': 'genericUser/change_contact_info.html'}, name='change_contact_info'),
	url(r'^retrieve_password/$', views.retrieve_password, name='retrieve_password'),
	url(r'^review_user/(?P<username>[\w-]+)/$', views.review_user, name='review_user'),
	url(r'^verify_contact_info/$', views.verify_contact_info, name='verify_contact_info'),
	url(r'^user_update/(?P<ID>\d+)/$', views.user_update, name='user_update'),
	url(r'^user_list/$', views.user_list, name='user_list'),
	url(r'^user_view/(?P<ID>\d+)/$', views.user_view, name='user_view'),
	url(r'^user_manager/$', views.user_manager, name='user_manager'),
	url(r'^announcement_create$', views.announcement_create, name='announcement_create'),
	url(r'^announcement_update/(?P<id>[0-9]+)/$', views.announcement_update, name='announcement_update'),
	url(r'^announcement_delete/(?P<id>[0-9]+)/$', views.announcement_delete, name='announcement_delete'),
	url(r'^announcement_list$', views.announcement_list, name='announcement_list'),
	url(r'^announcement/(?P<ID>[0-9]+)/$', views.announcement, name='announcement'),
	url(r'^qanda_create/$', views.qanda_create, name='qanda_create'),
	url(r'^qanda_update/(?P<id>[0-9]+)/$', views.qanda_update, name='qanda_update'),
	url(r'^qanda_delete/(?P<id>[0-9]+)/$', views.qanda_delete, name='qanda_delete'),
	url(r'^qanda_list$', views.qanda_list, name='qanda_list'),
	url(r'^api/', include(api_urlpatterns, namespace='api')),
	url(r'^resource/', include(resource_urlpatterns, namespace='resource')),
	url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
