# coding: utf-8
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

#class MixedPermissionModelViewSet(viewsets.ModelViewSet):
class MixedPermissionModelViewSet(object):
	'''
	Mixed permission base model allowing for action level
	permission control. Subclasses may define their permissions
	by creating a 'permission_classes_by_action' variable.

	Example:
	permission_classes_by_action = {'list': [AllowAny],
									'create': [IsAdminUser]}
	'''

	permission_classes_by_action = {}

	def get_permissions(self):
		try:
			# return permission_classes depending on `action`
			return [permission() for permission in self.permission_classes_by_action[self.action]]
		except KeyError:
			# action is not set return default permission_classes
			return [permission() for permission in self.permission_classes]

import json

class ReadsModelViewSetMixin(object):
	"""
	Reads a queryset.
	"""
	@action(
		detail=False,
		methods=['get'],
		url_name='reads',
		url_path='action/reads',
	)
	def reads(self, request, *args, **kwargs):
		pks = json.loads(request.query_params.get('pks'))
		queryset = self.queryset.filter(pk__in=pks)

		page = self.paginate_queryset(queryset)
		if page is not None:
			serializer = self.get_serializer(page, many=True)
			return self.get_paginated_response(serializer.data)

		serializer = self.get_serializer(queryset, many=True)
		return Response(serializer.data)
