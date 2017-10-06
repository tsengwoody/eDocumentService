# coding: utf-8
from django.core.urlresolvers import reverse, resolve
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render
import json

from genericUser.models import View

def view_permission(view):
	def decorator(request, *args, **kwargs):
		r = resolve(request.path)
		try:
			v = View.objects.get(namespace=r.namespace, url_name=r.url_name)
		except View.DoesNotExist:
			v = None
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
		if (v and v.check_permission(request.user)) or not v:
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
	return decorator

def http_response(view):
	def decorator(request, *args, **kwargs):
		rend_dict = {}
		rend_dict = view(request, *args, **kwargs)
		if request.is_ajax():
			if 'extra_list' not in rend_dict:
				rend_dict['extra_list'] = []
			response = {}
			if 'redirect_to' in rend_dict:
				response['redirect_to'] = rend_dict['redirect_to']
			elif 'content' in rend_dict:
				response['content'] = rend_dict['content']
			elif 'permission_denied' in rend_dict:
				response['permission_denied'] = rend_dict['permission_denied']
			elif 'download_path' in rend_dict:
				with open(rend_dict['download_path'], 'rb') as content_file:
					response = HttpResponse(content=content_file, )
				response['Content-Type'] = 'application/octet-stream'
				response['Content-Disposition'] = u'attachment; filename="{0}"'.format(rend_dict['download_filename']).encode('utf-8')
				return response
			response['status'] = rend_dict['status']
			response['message'] = rend_dict['message']
			for key in rend_dict['extra_list']:
				response[key] = rend_dict[key]
			return HttpResponse(json.dumps(response), content_type="application/json")
		else:
			if 'permission_denied' in rend_dict:
				template_name = 'user_category_check.html'
				return render(request, template_name, {})
			elif 'redirect_to' in rend_dict:
				return HttpResponseRedirect(rend_dict['redirect_to'])
			elif 'download_path' in rend_dict:
				with open(rend_dict['download_path'], 'rb') as content_file:
					response = HttpResponse(content=content_file, )
				response['Content-Type'] = 'application/octet-stream'
				response['Content-Disposition'] = u'attachment; filename="{0}"'.format(rend_dict['download_filename']).encode('utf-8')
				return response
			else:
				return render(request, rend_dict['template_name'], rend_dict)
	return decorator
