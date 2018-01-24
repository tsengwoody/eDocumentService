# coding: utf-8

from rest_framework import filters
from .models import *

class ServiceInfoExchangeFilter(filters.BaseFilterBackend):
	def filter_queryset(self, request, queryset, view):
		is_exchange = request.query_params.get('is_exchange')
		if is_exchange and exchange in ['true', 'True']:
			return queryset.filter(is_exchange=True)
		elif is_exchange and exchange in ['false', 'False']:
			return queryset.filter(is_exchange=False)
		else:
			return queryset

class ServiceInfoUserFilter(filters.BaseFilterBackend):
	def filter_queryset(self, request, queryset, view):
		user_id = request.query_params.get('user_id')
		if user_id:
			user = User.objects.get(id=user_id)
			return queryset.filter(user=user)
		else:
			return queryset

class AnnouncementCategoryFilter(filters.BaseFilterBackend):
	def filter_queryset(self, request, queryset, view):
		category = request.query_params.get('category')
		if category:
			return queryset.filter(category=category)
		else:
			return queryset

class AnnouncementNewestFilter(filters.BaseFilterBackend):

	def filter_queryset(self, request, queryset, view):
		newest = request.query_params.get('newest')
		if newest:
			return queryset.order_by('-datetime')[0:int(newest)]
		else:
			return queryset

class UserSelfOrManagerFilter(filters.BaseFilterBackend):
	def filter_queryset(self, request, queryset, view):
		if hasattr(request.user, 'is_manager') and request.user.is_manager:
			return queryset
		else:
			return queryset.filter(id=request.user.id)
