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

OrgFilter = KeyMapAttrFilterFactory(key = 'org_id', type = str, attr = 'org_id')
DisabilityCardOrgFilter = KeyMapAttrFilterFactory(key = 'org_id', type = str, attr = 'owner__org_id')

QAndACategoryFilter = KeyMapAttrFilterFactory(key='category', type=str, attr='category')

class AnnouncementNewestFilter(filters.BaseFilterBackend):

	def filter_queryset(self, request, queryset, view):
		newest = request.query_params.get('newest')
		if newest:
			return queryset.order_by('-datetime')[0:int(newest)]
		else:
			return queryset

from django.db.models import F,Q
class UserSelfOrManagerFilter(filters.BaseFilterBackend):
	def filter_queryset(self, request, queryset, view):
		owner_kwargs = {'id': request.user.id}
		org_kwargs = {'org': request.user.org.id}
		if request.user.has_perm('is_supermanager'):
			return queryset
		elif request.user.has_perm('is_manager'):
			return queryset.filter(
				Q(**org_kwargs)
				| Q(**owner_kwargs)
			)
		else:
			return queryset.filter(**owner_kwargs)

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
