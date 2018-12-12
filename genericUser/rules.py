import rules

@rules.predicate
def is_manager(user):
	return user.is_manager

@rules.predicate
def is_superuser(user):
	return user.is_superuser

rules.add_perm('is_superuser', is_superuser)
rules.add_perm('is_manager', is_manager)