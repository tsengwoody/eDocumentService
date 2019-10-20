<template>
	<div>
		<h2>書籍管理</h2>
		<book_manager_org :org="org">
		</book_manager_org>
	</div>
</template>

<script>
	module.exports = {
		components: {
			'book_manager_org': components['book_manager_org'],
		},
		data(){
			return {
				org: {},
			}
		},
		metaInfo: {
			title: '書籍管理',
		},
		mounted(){
			genericUserAPI.organizationRest.read(user.id)
			.then(res => {
				this.org = res.data;
			})
			.catch(res => {
				alertmessage('error', o2j(res.response.data));
			})
		},
	}
</script>