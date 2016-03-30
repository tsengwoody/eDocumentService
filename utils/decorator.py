from django.http import HttpResponseRedirect
def user_category_check(category):
	def user_category_out(view):
		def user_category_in(request, *args, **kwargs):
			if not request.user.is_authenticated():
				return HttpResponseRedirect('/auth/login')
			if category == 'editor' and request.user.is_editor():
				return view(request, *args, **kwargs)
			elif category == 'guest' and request.user.is_guest():
				return view(request, *args, **kwargs)
			else:
				return HttpResponseRedirect('/auth/login')
		return user_category_in
	return user_category_out