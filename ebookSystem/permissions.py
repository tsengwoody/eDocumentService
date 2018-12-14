# coding: utf-8
from __future__ import unicode_literals, absolute_import

from rest_framework import permissions

class ManagerOrOwner(permissions.BasePermission):

	def has_permission(self, request, view):
		return True

	def has_object_permission(self, request, view, obj):
		is_manager = hasattr(request.user, 'is_manager') and request.user.is_manager
		is_owner = obj.owner == request.user
		return is_manager or is_owner

class BookDataPermission(permissions.BasePermission):

	def has_permission(self, request, view):
		if request.method in permissions.SAFE_METHODS:
			return True

	def has_object_permission(self, request, view, obj):
		if request.method in permissions.SAFE_METHODS:
			return True

class EBookDataPermission(permissions.BasePermission):

	def has_permission(self, request, view):
		if request.method in permissions.SAFE_METHODS:
			return True

	def has_object_permission(self, request, view, obj):
		if request.method in permissions.SAFE_METHODS:
			return True
