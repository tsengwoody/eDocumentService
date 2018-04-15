# coding: utf-8
import mimetypes
import os

from django.http import FileResponse
from django.http import Http404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.decorators import detail_route, list_route
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

class Resource(APIView):
	resourceClass = None

	def get_object(self, pk):
		try:
			return self.resourceClass.objects.get(pk=pk)
		except self.resourceClass.DoesNotExist:
			raise Http404

	def get_resource(self, fullpath):
		if not os.path.exists(fullpath):
			raise Http404(('"%(fullpath)s" does not exist') % {'fullpath': fullpath})
		# Respect the If-Modified-Since header.
		statobj = os.stat(fullpath)
		content_type, encoding = mimetypes.guess_type(fullpath)
		content_type = content_type or 'application/octet-stream'
		response = FileResponse(open(fullpath, 'rb'), content_type='application/octet-stream')
		response['Content-Disposition'] = u'attachment; filename="{0}"'.format(os.path.basename(fullpath)).encode('utf-8')
		#response["Last-Modified"] = http_date(statobj.st_mtime)
		#if stat.S_ISREG(statobj.st_mode):
			#response["Content-Length"] = statobj.st_size
		if encoding:
			response["Content-Encoding"] = encoding
		return response

	def post_resource(self, fullpath, file):
		dirname = os.path.dirname(fullpath)
		if not os.path.exists(dirname):
			os.makedirs(dirname, 0755)
		with open(fullpath, 'wb+') as destination:
			for chunk in file.chunks():
				destination.write(chunk)
		return Response(status=status.HTTP_202_ACCEPTED)

from django.views.decorators.csrf import csrf_exempt

class ResourceViewSet(Resource):

	@detail_route(
		methods=['get', 'post'],
		url_name='resource',
		url_path='resource/(?P<dir>[\w]+)/(?P<resource>[\d\w]+)',
	)
	def resource(self, request, pk=None, dir=None, resource=None):
		obj = self.get_object()
		fullpath = self.get_fullpath(obj, dir, resource)
		if request.method == 'GET':
			return self.get_resource(fullpath)
		if request.method == 'POST':
			return self.post_resource(fullpath, request.FILES['object'])