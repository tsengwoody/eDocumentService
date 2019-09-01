<template>
	<div>
		<h2>校對服務</h2>
		<service_org :org_id="user.org" :choice_org="true">
		</service_org>
	</div>
</template>

<script>
	module.exports = {
		components: {
			'service_org': components['service_org'],
		},
		metaInfo: {
			title: '一般校對',
		},
	}
</script>