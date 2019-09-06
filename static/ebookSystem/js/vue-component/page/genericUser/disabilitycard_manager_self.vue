<template>
	<div>
		<h2>身障手冊管理</h2>
		<disabilitycard_manager_org :org_id="user.org">
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
			}
		},
		metaInfo: {
			title: '身障手冊管理',
		},
		mounted(){
		},
	}
</script>