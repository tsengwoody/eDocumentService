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
	return s
	#return s.encode('utf8')

def boolean(s):
	if s in ['True', 'true',]:
		return True
	elif s in ['False', 'false',]:
		return False

def period(s):
	from json import loads
	from django.utils import timezone
	period = loads(s)
	try:
		begin = period['begin'].split('-')
		begin = [ int(v) for v in begin ]
		begin = timezone.datetime(begin[0], begin[1], begin[2])
	except:
		begin = None
	try:
		end = period['end'].split('-')
		end = [ int(v) for v in end ]
		end = timezone.datetime(end[0], end[1], end[2])
	except:
		end = None
	print(begin)
	print(end)
	return {
		'begin': begin,
		'end': end,
	}

def items(s):
	from json import loads
	return loads(s)

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
				return []

	return BaseFilter

def PeriodFilterFactory(key, attr):
	class BaseFilter(filters.BaseFilterBackend):
		def __init__(self):
			self.key = key
			self.attr = attr

		def filter_queryset(self, request, queryset, view):
			value = request.query_params.get(self.key)
			if not value:
				return queryset
			try:
				if value=='null':
					return queryset
				else:
					self.value = period(value)
				kwargs = {}
				if self.value['begin']:
					kwargs[self.attr +'__gte'] = self.value['begin']
				if self.value['end']:
					kwargs[self.attr +'__lte'] = self.value['end']
				return queryset.filter(**kwargs)
			except BaseException as e:
				return queryset

	return BaseFilter

def ItemsFilterFactory(key, attr):
	class BaseFilter(filters.BaseFilterBackend):
		def __init__(self):
			self.key = key
			self.attr = attr

		def filter_queryset(self, request, queryset, view):
			value = request.query_params.get(self.key)
			print(value)
			if not value:
				return queryset
			try:
				if value=='null':
					return queryset
				else:
					self.value = items(value)
				return queryset.filter(pk__in=self.value)
			except BaseException as e:
				return queryset

	return BaseFilter

OwnerOrgManagerFilter = PermissionFilterFactory(attr='owner')
