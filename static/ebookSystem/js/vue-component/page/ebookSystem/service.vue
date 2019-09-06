<template>
	<div>
		<h2>校對服務</h2>
		<service_org org_id="1" :choice_org="false">
		</service_org>
	</div>
</template>

<script>
	module.exports = {
		components: {
			'service_org': components['service_org'],
		},
		metaInfo: {
			title: '校對服務',
		},
	}
</script>