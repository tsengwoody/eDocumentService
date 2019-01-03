<template>
	<div>
		<h2>書籍管理</h2>
		<book_manager_org :org_id="user.org">
		</book_manager_org>
	</div>
</template>

<script>
	module.exports = {
		components: {
			'book_manager_org': components['book_manager_org'],
		},
		data: function() {
			return {
			}
		},
		mounted: function () {
			document.title = '書籍管理';
		},
	}
</script>