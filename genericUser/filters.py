# coding: utf-8

from rest_framework import filters
from utils.filters import KeyMapAttrFilterFactory, convert_bool, convert_unicode
from .models import *

# ['disabilitycard_manager', ]
DisabilityCardActiveFilter = KeyMapAttrFilterFactory(key='is_active', type=convert_bool, attr='is_active')

# ['', ]
ServiceInfoExchangeFilter = KeyMapAttrFilterFactory(key='is_exchange', type=convert_bool, attr='is_exchange')

# ['', ]
OwnerFilter = KeyMapAttrFilterFactory(key = 'owner_id', type = str, attr = 'owner_id')

AnnouncementCategoryFilter = KeyMapAttrFilterFactory(key='category', type=convert_unicode, attr='category')
QAndACategoryFilter = KeyMapAttrFilterFactory(key='category', type=str, attr='category')

'''class AnnouncementCategoryFilter(filters.BaseFilterBackend):
	def filter_queryset(self, request, queryset, view):
		category = request.query_params.get('category')
		if category:
			return queryset.filter(category=category)
		else:
			return queryset'''

class AnnouncementNewestFilter(filters.BaseFilterBackend):

	def filter_queryset(self, request, queryset, view):
		newest = request.query_params.get('newest')
		if newest:
			return queryset.order_by('-datetime')[0:int(newest)]
		else:
			return queryset

class UserSelfOrManagerFilter(filters.BaseFilterBackend):
	def filter_queryset(self, request, queryset, view):
		if request.user.has_perm('is_manager'):
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
