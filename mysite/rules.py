# coding: utf-8
from __future__ import absolute_import
import rules


@rules.predicate
def is_supermanager(user):
	return getattr(user, 'is_supermanager', False)


@rules.predicate
def is_superuser(user):
	return getattr(user, 'is_superuser', False)


@rules.predicate
def is_manager(user):
	return getattr(user, 'is_manager', False)


@rules.predicate
def is_editor(user):
	return getattr(user, 'is_editor', False)


@rules.predicate
def is_guest(user):
	return getattr(user, 'is_guest', False)


@rules.predicate
def is_self(user, obj):
	if obj:
		return user == obj
	else:
		return False


# 判斷物件是否為該人員
@rules.predicate
def is_owner_object(user, obj):
	if obj:
		if hasattr(obj, 'owner'):
			return user == obj.owner
		else:
			return False
	else:
		return False


# 判斷物件是否為該單位人員可管理
@rules.predicate
def is_org_object(user, obj):
	if obj:
		try:
			return user.org == obj.owner.org
		except:
			return False
	else:
		return False


rules.add_perm('is_superuser', is_superuser)
rules.add_perm('is_supermanager', is_supermanager)
rules.add_perm('is_manager', is_manager)
rules.add_perm('is_editor', is_editor)
rules.add_perm('is_guest', is_guest)
rules.add_perm('is_self', is_self)
rules.add_perm('is_owner_object', is_owner_object)
rules.add_perm('is_org_object', is_org_object)
rules.add_perm('is_manager_object',
	(is_owner_object | (is_org_object & is_manager) | is_supermanager))
