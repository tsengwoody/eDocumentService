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

rules.add_perm('is_superuser', is_superuser)
rules.add_perm('is_manager', is_manager)
rules.add_perm('is_editor', is_editor)
rules.add_perm('is_guest', is_guest)
