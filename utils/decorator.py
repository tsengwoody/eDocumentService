# coding: utf-8
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render

def user_category_check(category):
	def user_category_out(view):
		def user_category_in(request, *args, **kwargs):
			redirect_to = None
			if not request.user.is_authenticated():
				template_name = 'user_category_check.html'
				redirect_to = reverse('login')
				message = u'您尚未登錄'
				return render(request, template_name, locals())
			if 'editor' in category and request.user.is_editor():
				return view(request, *args, **kwargs)
			elif 'guest' in category and request.user.is_guest():
				return view(request, *args, **kwargs)
			elif 'scaner' in category and request.user.is_scaner:
				return view(request, *args, **kwargs)
			elif 'manager' in category and request.user.is_manager:
				return view(request, *args, **kwargs)
			else:
				template_name = 'user_category_check.html'
				redirect_to = reverse('login')
				message = u'帳號無權限'
				return render(request, template_name, locals())
		return user_category_in
	return user_category_out