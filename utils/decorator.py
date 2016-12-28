# coding: utf-8
from django.core.urlresolvers import reverse
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render
import json

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
			if 'user' in category and request.user.authentication():
				return view(request, *args, **kwargs)
			elif 'editor' in category and request.user.is_editor:
				return view(request, *args, **kwargs)
			elif 'guest' in category and request.user.is_guest:
				return view(request, *args, **kwargs)
			elif 'manager' in category and request.user.is_manager:
				return view(request, *args, **kwargs)
			elif 'advanced_editor' in category and request.user.is_advanced_editor:
				return view(request, *args, **kwargs)
			elif 'staff' in category and request.user.is_staff:
				return view(request, *args, **kwargs)
			elif 'superuser' in category and request.user.is_superuser:
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
		rend_dict = {}
		rend_dict = view(request, *args, **kwargs)
		if request.is_ajax():
			if 'extra_list' not in rend_dict:
				rend_dict['extra_list'] = []
			response = {}
			response['status'] = rend_dict['status']
			response['message'] = rend_dict['message']
			if 'redirect_to' in rend_dict:
				response['redirect_to'] = rend_dict['redirect_to']
			if 'permission_denied' in rend_dict:
				response['permission_denied'] = rend_dict['permission_denied']
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

from .validate import audio_code
from django.core.cache import cache
from mysite.settings import BASE_DIR
import os
def audio_code_valid(view):
	def decorator(request, *args, **kwargs):
		if request.method == 'POST':
			if request.POST.has_key('code') and request.POST.has_key('UUID') and request.POST['code'] == cache.get(request.POST['UUID']):
				os.remove(BASE_DIR +'/static/audio_code/' +request.POST['UUID'] +'.mp3')
				return view(request, *args, **kwargs)
			else:
				if request.is_ajax():
					response = {}
					response['status'] = 'error'
					response['message'] = u'驗證碼錯誤'
					return HttpResponse(json.dumps(response), content_type="application/json")
				else:
					template_name = 'audio_code_error.html'
					return render(request, template_name, locals())
		if request.method == 'GET':
			[UUID, code] = audio_code()
			UUIDDict = {'UUID':UUID}
			kwargs.update(UUIDDict)
			return view(request, *args, **kwargs)
	return decorator