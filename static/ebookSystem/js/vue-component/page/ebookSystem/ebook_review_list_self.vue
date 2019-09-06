<template>
	<div>
		<h2>校對文件審核</h2>
		<ebook_review_list_org :org_id="user.org">
		</ebook_review_list_org>
	</div>
</template>

<script>
	module.exports = {
		components: {
			'ebook_review_list_org': components['ebook_review_list_org'],
		},
		data(){
			return {
			}
		},
		metaInfo: {
			title: '校對文件審核',
		},
	}
</script>