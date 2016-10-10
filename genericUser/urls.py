from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^apply_document/$', views.apply_document, name='apply_document'),
	url(r'^func_desc/$', views.func_desc, name='func_desc'),
	url(r'^org_info$', views.org_info, name='org_info'),
	url(r'^license/$', views.license, name='license'),
	url(r'^create_document/$', views.create_document, name='create_document'),
	url(r'^upload_progress/$', views.upload_progress, name='upload_progress'),
	url(r'^event_list/$', views.event_list, name='event_list'),
	url(r'^contact_us/$', views.contact_us, {'template_name': 'genericUser/contact_us.html'}, name='contact_us'),
	url(r'^servicehours_list/(?P<username>[\w-]+)/$', views.servicehours_list, {'template_name': 'genericUser/servicehours_list.html'}, name='servicehours_list'),
	url(r'^info/$', views.info, {'template_name': 'genericUser/info.html'}, name='info'),
	url(r'^change_contact_info/$', views.change_contact_info, {'template_name': 'genericUser/change_contact_info.html'}, name='change_contact_info'),
	url(r'^set_role/$', views.set_role, {'template_name': 'genericUser/set_role.html'}, name='set_role'),
	url(r'^review_user/(?P<username>[\w-]+)/$', views.review_user, name='review_user'),
	url(r'^revise_content/$', views.revise_content, name='revise_content'),
	url(r'^verify_contact_info/$', views.verify_contact_info, name='verify_contact_info'),
	url(r'^test_message/$', views.test_message, {'template_name': 'genericUser/test_message.html'}, name='test_message'),
]
