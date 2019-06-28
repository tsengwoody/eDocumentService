# coding: utf-8
import datetime
import mimetypes
import os
import shutil

from django.http import FileResponse
from django.http import Http404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.decorators import detail_route, list_route
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

def sizeof_fmt(num, suffix='B'):
	for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
		if abs(num) < 1024.0:
			return "%3.1f%s%s" % (num, unit, suffix)
		num /= 1024.0
	return "%.1f%s%s" % (num, 'Yi', suffix)

class Resource(APIView):

	def resource(self, request, dir, resource):
		fullpath = self.get_fullpath(dir, resource)
		if request.method == 'GET':
			try:
				return self.get_resource(fullpath)
			except OSError as e:
				return Response(data={'detail' :unicode(e)}, status=status.HTTP_404_NOT_FOUND)
		if request.method == 'POST':
			try:
				return self.post_resource(fullpath, request.FILES['object'])
			except OSError as e:
				return Response(data={'detail' :unicode(e)}, status=status.HTTP_404_NOT_FOUND)

	def category(self, request, dir):
		fullpath = self.get_fullpath(dir, resource='')
		try:
			return self.get_resource_list(fullpath)
		except OSError as e:
			return Response(data={'detail' :unicode(e)}, status=status.HTTP_404_NOT_FOUND)

	def get_resource(self, fullpath):
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
			os.makedirs(dirname, 0o755)
		with open(fullpath, 'wb+') as destination:
			for chunk in file.chunks():
				destination.write(chunk)
		return Response(status=status.HTTP_202_ACCEPTED)

	def delete_resource(self, fullpath):
		os.remove(fullpath)
		return Response(data={}, status=status.HTTP_202_ACCEPTED)

	def get_resource_list(self, fullpath):
		res = []
		resources = os.listdir(fullpath)
		for index, resource in enumerate(resources):
			resource_path = os.path.join(fullpath, resource)
			resource_stat = os.stat(resource_path)
			content_type, encoding = mimetypes.guess_type(fullpath)
			#content_type = content_type or resource.split('.')[-1]
			res.append({
				'name': resource,
				'mtime': datetime.datetime.fromtimestamp(resource_stat.st_mtime),
				'size': sizeof_fmt(resource_stat.st_size),
				'content_type': content_type,
			})

		return Response(data=res, status=status.HTTP_202_ACCEPTED)

from django.views.decorators.csrf import csrf_exempt

class ResourceViewSet(Resource):

	@list_route(
		methods=['get', 'post'],
		url_name='resource-list',
		url_path='resource/(?P<dir>[\d\w]+)/(?P<resource>.+)',
	)
	def resource_list(self, request, pk=None, dir=None, resource=None):
		fullpath = self.get_fullpath_list(dir, resource)
		if request.method == 'GET':
			try:
				return self.get_resource(fullpath)
			except OSError as e:
				return Response(data={'detail' :unicode(e)}, status=status.HTTP_404_NOT_FOUND)
		if request.method == 'POST':
			try:
				return self.post_resource(fullpath, request.FILES['object'])
			except OSError as e:
				return Response(data={'detail' :unicode(e)}, status=status.HTTP_404_NOT_FOUND)

	@detail_route(
		methods=['get', 'post', 'delete'],
		url_name='resource',
		url_path='resource/(?P<dir>[\d\w]+)/(?P<resource>.+)',
	)
	def resource(self, request, pk=None, dir=None, resource=None):
		obj = self.get_object()
		fullpath = self.get_fullpath(obj, dir, resource)
		if request.method == 'GET':
			try:
				return self.get_resource(fullpath)
			except OSError as e:
				return Response(data={'detail' :unicode(e)}, status=status.HTTP_404_NOT_FOUND)
		if request.method == 'POST':
			try:
				return self.post_resource(fullpath, request.FILES['object'])
			except OSError as e:
				return Response(data={'detail' :unicode(e)}, status=status.HTTP_404_NOT_FOUND)
		if request.method == 'DELETE':
			try:
				return self.delete_resource(fullpath)
			except OSError as e:
				return Response(data={'detail' :unicode(e)}, status=status.HTTP_404_NOT_FOUND)

	@list_route(
		methods=['get'],
		url_name='category-list',
		url_path='resource/(?P<dir>[\d\w]+)',
	)
	def category_list(self, request, pk=None, dir=None):
		try:
			return self.get_resource_list()
		except OSError as e:
			return Response(data={'detail' :unicode(e)}, status=status.HTTP_404_NOT_FOUND)

	@detail_route(
		methods=['get'],
		url_name='category',
		url_path='resource/(?P<dir>[\d\w]+)',
	)
	def category(self, request, pk=None, dir=None):
		obj = self.get_object()
		fullpath = self.get_fullpath(obj, dir, resource='')
		try:
			return self.get_resource_list(fullpath)
		except OSError as e:
			return Response(data={'detail' :unicode(e)}, status=status.HTTP_404_NOT_FOUND)
