<template>
	<div>
		<h2>管理書籍類型</h2>
		<category_manager_org :org_id="user.org">
		</category_manager_org>
	</div>
</template>

<script>
	module.exports = {
		components: {
			'category_manager_org': components['category_manager_org'],
		},
		data: function() {
			return {
			}
		},
		mounted: function () {
			document.title = '管理書籍類型';
		},
	}
</script>