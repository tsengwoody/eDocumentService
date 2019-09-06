<template>
	<div>
		<h2>服務時數確認</h2>
		<serviceinfo_list_check_org :org_id="user.org">
		</serviceinfo_list_check_org>
	</div>
</template>

<script>
	module.exports = {
		components: {
			'serviceinfo_list_check_org': components['serviceinfo_list_check_org'],
		},
		data(){
			return {
			}
		},
		metaInfo: {
			title: '服務時數確認(各單位)',
		},
		mounted(){
		},
	}
</script>