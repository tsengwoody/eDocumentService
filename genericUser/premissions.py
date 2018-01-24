# coding: utf-8
from __future__ import unicode_literals, absolute_import

from rest_framework import permissions

class UserDataPermission(permissions.BasePermission):

	def has_permission(self, request, view):
		if request.method in permissions.SAFE_METHODS:
			return True
		if request.method in ['POST', 'PUT', 'PATCH']:
			return True

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
