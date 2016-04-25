# coding: utf-8
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render

def user_category_check(category):
	def user_category_out(view):
		def user_category_in(request, *args, **kwargs):
			response = {}
			if not request.user.is_authenticated():
				template_name = 'user_category_check.html'
				redirect_to = reverse('login')
				status = 'error'
				message = u'您尚未登錄'
				response['redirect_to'] = redirect_to
				response['status'] = status
				response['message'] = message
				if request.is_ajax():
					return HttpResponse(json.dumps(response), content_type="application/json")
				else:
					return render(request, template_name, locals())
			if 'user' in category and request.user.is_authenticated():
				return view(request, *args, **kwargs)
			elif 'editor' in category and request.user.is_editor:
				return view(request, *args, **kwargs)
			elif 'guest' in category and request.user.is_guest:
				return view(request, *args, **kwargs)
			elif 'scaner' in category and request.user.is_scaner:
				return view(request, *args, **kwargs)
			elif 'manager' in category and request.user.is_manager:
				return view(request, *args, **kwargs)
			else:
				template_name = 'user_category_check.html'
				redirect_to = reverse('login')
				status = 'error'
				message = u'帳號無權限'
				response['redirect_to'] = redirect_to
				response['status'] = status
				response['message'] = message
				if request.is_ajax():
					return HttpResponse(json.dumps(response), content_type="application/json")
				else:
					return render(request, template_name, locals())
		return user_category_in
	return user_category_out

def http_response(view):
	def decorator(request, *args, **kwargs):
		rend_dict = view(request, *args, **kwargs)
		print rend_dict
		return render(request, 'ebookSystem/search_book.html', rend_dict)
	return decorator