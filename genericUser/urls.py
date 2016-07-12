from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^apply_document/$', views.apply_document, name='apply_document'),
	url(r'^create_document/$', views.create_document, name='create_document'),
	url(r'^upload_progress/$', views.upload_progress, name='upload_progress'),
	url(r'^contact_us/$', views.contact_us, {'template_name': 'genericUser/contact_us.html'}, name='contact_us'),
	url(r'^info/$', views.info, {'template_name': 'genericUser/info.html'}, name='info'),
	url(r'^info_change/$', views.info_change, {'template_name': 'genericUser/info_change.html'}, name='info_change'),
	url(r'^set_role/$', views.set_role, {'template_name': 'genericUser/set_role.html'}, name='set_role'),
	url(r'^review_user/(?P<username>[\w-]+)/$', views.review_user, name='review_user'),
	url(r'^revise_content/$', views.revise_content, name='revise_content'),
	url(r'^test_message/$', views.test_message, {'template_name': 'genericUser/test_message.html'}, name='test_message'),
]
