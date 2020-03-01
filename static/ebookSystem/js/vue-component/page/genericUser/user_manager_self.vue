<template>
	<div>
		<h2>使用者管理</h2>
		<user_manager_org :org="org">
		</user_manager_org>
	</div>
</template>

<script>
	module.exports = {
		components: {
			'user_manager_org': components['user_manager_org'],
		},
		data(){
			return {
				org: {},
			}
		},
		metaInfo: {
			title: '使用者管理',
		},
		mounted(){
			genericUserAPI.organizationRest.read(user.org)
			.then(res => {
				this.org = res.data;
			})
			.catch(res => {
				alertmessage('error', o2j(res.response.data));
			})
		},
	}
</script>