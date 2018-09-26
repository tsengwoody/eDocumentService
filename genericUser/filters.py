# coding: utf-8

from django.db.models import F,Q
from rest_framework import filters
from .models import *

class DisabilityCardActiveFilter(filters.BaseFilterBackend):
	def filter_queryset(self, request, queryset, view):
		is_active = request.query_params.get('is_active')
		if is_active and is_active in ['true', 'True']:
			return queryset.filter(is_active=True)
		elif is_active and is_active in ['false', 'False']:
			return queryset.filter(is_active=False)
		else:
			return queryset

class ServiceInfoExchangeFilter(filters.BaseFilterBackend):
	def filter_queryset(self, request, queryset, view):
		is_exchange = request.query_params.get('is_exchange')
		if is_exchange and is_exchange in ['true', 'True']:
			return queryset.filter(is_exchange=True)
		elif is_exchange and is_exchange in ['false', 'False']:
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

class UserOrganizationFilter(filters.BaseFilterBackend):
	def filter_queryset(self, request, queryset, view):
		org = request.query_params.get('org')
		if org:
			return queryset.filter(org=org)
		else:
			return queryset

class UserAuthFilter(filters.BaseFilterBackend):
	def filter_queryset(self, request, queryset, view):
		auth = request.query_params.get('auth')
		if auth:
			if auth == 'false' or auth == 'False':
				return queryset.filter(
					Q(auth_email=False)
					| Q(auth_phone=False)
				).filter(is_editor=False)
			elif auth == 'true' or auth == 'True':
				return queryset.filter(
					Q(auth_email=True)
					& Q(auth_phone=True)
				).filter(is_editor=False)
			else:
				return queryset
		else:
			return queryset

class UserRoleFilter(filters.BaseFilterBackend):
	def filter_queryset(self, request, queryset, view):
		role = request.query_params.get('role')
		if role:
			if role == 'guest':
				return queryset.filter(is_guest=True)
			elif role == 'editor':
				return queryset.filter(is_editor=True)
			elif role == 'all':
				return queryset
		else:
			return queryset

class QAndACategoryFilter(filters.BaseFilterBackend):
	def filter_queryset(self, request, queryset, view):
		category = request.query_params.get('category')
		if category:
			return queryset.filter(category=category)
		else:
			return queryset
