<template>
	<div>
		<h2>上傳文件審核</h2>
		<book_review_list_org :org_id="user.org">
		</book_review_list_org>
	</div>
</template>

<script>
	module.exports = {
		components: {
			'book_review_list_org': components['book_review_list_org'],
		},
		metaInfo: {
			title: '上傳文件審核',
		},
	}
</script>