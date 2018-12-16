from django.utils.deprecation import MiddlewareMixin
class CustomHeaderMiddleware(MiddlewareMixin):
	def process_response(self, request, response):
		response['Access-Control-Allow-Origin'] = '*'
		return response

class CustomHeader2Middleware(object):
	def __init__(self, get_response):
		self.get_response = get_response

	def __call__(self, request):
		response = self.get_response(request)
		response['Access-Control-Allow-Origin'] = '*'
		return response
