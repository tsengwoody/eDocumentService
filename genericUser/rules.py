# coding: utf-8
from __future__ import absolute_import
import rules

@rules.predicate
def is_manager(user):
	return user.is_manager

@rules.predicate
def is_superuser(user):
	return user.is_superuser

@rules.predicate
def is_editor(user):
	return user.is_editor

@rules.predicate
def is_guest(user):
	return user.is_guest

@rules.predicate
def is_self(user, obj):
	if obj:
		return user == obj
	else:
		return True

# 判斷物件是否為該人員
@rules.predicate
def is_owner_object(user, obj):
	if obj:
		return user == obj.owner
	else:
		return True

# 判斷物件是否為該單位人員可管理
@rules.predicate
def is_org_object(user, obj):
	if obj:
		return user.org == obj.owner.org
	else:
		return True

rules.add_perm('is_superuser', is_superuser)
rules.add_perm('is_manager', is_manager)
rules.add_perm('is_editor', is_editor)
rules.add_perm('is_guest', is_guest)
rules.add_perm('is_self', is_self)
rules.add_perm('is_owner_object', is_owner_object)
rules.add_perm('is_org_object', is_org_object)
rules.add_perm(
	'is_manager_object',
	(is_owner_object | (is_org_object & is_manager))
)
