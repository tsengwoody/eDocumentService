# coding: utf-8
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
import json
def user_category_check(category):
	def user_category_out(view):
		def user_category_in(request, *args, **kwargs):
			response = {}
			if not request.user.is_authenticated():
				redirect_to = reverse('login')
				response['status'] = 'error'
				response['message'] = u'您尚未登錄'
				response['redirect_to'] = redirect_to
				if request.is_ajax():
					return HttpResponse(json.dumps(response), content_type="application/json");
				else:
					return HttpResponseRedirect(redirect_to)
			if category == 'editor' and request.user.is_editor():
				return view(request, *args, **kwargs)
			elif category == 'guest' and request.user.is_guest():
				return view(request, *args, **kwargs)
			else:
				redirect_to = reverse('login')
				response['status'] = 'error'
				response['message'] = u'您的帳號無權限查看此頁'
				response['redirect_to'] = redirect_to
				if request.is_ajax():
					return HttpResponse(json.dumps(response), content_type="application/json");
				else:
					return HttpResponseRedirect(redirect_to)
		return user_category_in
	return user_category_out