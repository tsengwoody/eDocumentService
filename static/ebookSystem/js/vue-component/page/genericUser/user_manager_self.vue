<template>
	<div>
		<h2>使用者管理</h2>
		<user_manager_org :org_id="user.org">
		</user_manager_org>
	</div>
</template>

<script>
	module.exports = {
		components: {
			'user_manager_org': components['user_manager_org'],
		},
		data: function() {
			return {
			}
		},
		mounted: function () {
			document.title = '使用者管理';
		},
	}
</script>