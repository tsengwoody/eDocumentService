# coding: utf-8
from __future__ import unicode_literals, absolute_import

from rest_framework import permissions

from .rules import rules
def RuleORPermission(rule_methods):
	class PermissionClass(permissions.BasePermission):
		def has_permission(self, request, view):
			perm = False
			for rule, methods in rule_methods:
				if '__all__' in methods:
					methods.extend(['GET', 'POST', 'PUT', 'PATCH', 'DELETE',])
				perm = perm or (request.user.has_perm(rule))
			return perm

		def has_object_permission(self, request, view, obj):
			# πÔ rule ¿À¨d
			perm = False
			for rule, methods in rule_methods:
				if '__all__' in methods:
					methods.extend(['GET', 'POST', 'PUT', 'PATCH', 'DELETE',])
				perm = perm or (request.user.has_perm(rule, obj) and request.method in methods)

			return perm

	return PermissionClass

class UserDataPermission(permissions.BasePermission):
	def has_permission(self, request, view):
		if request.method in permissions.SAFE_METHODS:
			return True
		elif request.method in ['POST', 'PUT', 'PATCH']:
			return True
		else:
			return False

	def has_object_permission(self, request, view, obj):
		if obj==request.user or (hasattr(request.user, 'is_manager') and request.user.is_manager):
			return True

class ServiceInfoDataPermission(permissions.BasePermission):
	pass

class IsManagerOrReadOnly(permissions.BasePermission):

	def has_permission(self, request, view):
		if request.method in permissions.SAFE_METHODS:
			return True
		return hasattr(request.user, 'is_manager') and request.user.is_manager

	def has_object_permission(self, request, view, obj):
		if request.method in permissions.SAFE_METHODS:
			return True
		return hasattr(request.user, 'is_manager') and request.user.is_manager

class IsManager(permissions.BasePermission):

	def has_permission(self, request, view):
		return hasattr(request.user, 'is_manager') and request.user.is_manager

	def has_object_permission(self, request, view, obj):
		return hasattr(request.user, 'is_manager') and request.user.is_manager
