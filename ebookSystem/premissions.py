# coding: utf-8
from __future__ import unicode_literals, absolute_import

from rest_framework import permissions

class EBookIsSelf(permissions.BasePermission):

	def has_permission(self, request, view):
		return obj.editor == request.user

	def has_object_permission(self, request, view, obj):
		return obj.editor == request.user
