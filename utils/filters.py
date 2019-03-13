# coding: utf-8

from rest_framework import filters

# attr 為 owner 的名稱，亦即 owner 可不為 'owner'
def PermissionFilterFactory(attr):
	from django.db.models import F,Q
	class OwnerOrgManagerPermissionFilter(filters.BaseFilterBackend):
		def filter_queryset(self, request, queryset, view):
			owner_id = attr +'_id'
			owner_kwargs = {owner_id: request.user.id}
			org_kwargs = {owner_id +'__org': request.user.org.id}
			if request.user.has_perm('is_supermanager'):
				return queryset
			elif request.user.has_perm('is_manager'):
				return queryset.filter(
					Q(**org_kwargs)
					| Q(**owner_kwargs)
				)
			else:
				return queryset.filter(**owner_kwargs)

	return OwnerOrgManagerPermissionFilter

def convert_bool(s):
	if s in ['True', 'true',]:
		return True
	elif s in ['False', 'false',]:
		return False

def convert_unicode(s):
	return s.encode('utf8')

def KeyMapAttrFilterFactory(key, type, attr):
	class BaseFilter(filters.BaseFilterBackend):
		def __init__(self):
			self.key = key
			self.type = type
			self.attr = attr

		def filter_queryset(self, request, queryset, view):
			value = request.query_params.get(self.key)
			if not value:
				return queryset
			try:
				if value=='null':
					self.value = None
				else:
					self.value = self.type(value)
				kwargs = {
					self.attr: self.value,
				}
				return queryset.filter(**kwargs)
			except BaseException as e:
				return queryset

	return BaseFilter

OwnerOrgManagerFilter = PermissionFilterFactory(attr='owner')
