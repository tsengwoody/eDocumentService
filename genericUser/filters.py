# coding: utf-8

from rest_framework import filters
from .models import *

class ServiceInfoUserFilter(filters.BaseFilterBackend):
	def filter_queryset(self, request, queryset, view):
		user_id = request.query_params.get('user_id')
		if user_id:
			user = User.objects.get(id=user_id)
			return queryset.filter(user=user)
		else:
			return queryset
