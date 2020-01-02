<template>
	<div>
		<h2>身障手冊管理</h2>
		<disabilitycard_manager_org :org="org">
		</disabilitycard_manager_org>
	</div>
</template>

<script>
	module.exports = {
		components: {
			'disabilitycard_manager_org': components['disabilitycard_manager_org'],
		},
		data(){
			return {
				org: {},
			}
		},
		metaInfo: {
			title: '身障手冊管理',
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