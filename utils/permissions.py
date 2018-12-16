# coding: utf-8
from __future__ import unicode_literals, absolute_import

from rest_framework import permissions
from mysite.rules import rules

def RuleORPermissionFactory(action, rule_list):
	class ListPermissionClass(permissions.BasePermission):
		def has_permission(self, request, view):
			if '__read__' in rule_list and request.method in permissions.SAFE_METHODS:
				return True
			if '__write__' in rule_list and (not request.method in permissions.SAFE_METHODS):
				return True
			perm = False
			for rule in rule_list:
				perm = perm or request.user.has_perm(rule)
			return perm

	class DetailPermissionClass(permissions.BasePermission):
		def has_object_permission(self, request, view, obj):
			if '__read__' in rule_list and request.method in permissions.SAFE_METHODS:
				return True
			if '__write__' in rule_list and (not request.method in permissions.SAFE_METHODS):
				return True
			perm = False
			for rule in rule_list:
				perm = perm or request.user.has_perm(rule, obj)
			return perm

	class DefaultPermissionClass(permissions.BasePermission):
		def has_permission(self, request, view):
			return False

	if action=='list':
		return ListPermissionClass
	elif action=='detail':
		return DetailPermissionClass
	else:
		return DefaultPermissionClass
