<template>
	<div>
		<h2>志工服務時數統計</h2>
			<statistics-serviceinfo
				:org="org"
			></statistics-serviceinfo>
		</template>
	</div>
</template>

<script>
	module.exports = {
		components: {
			panelGroup: components['panel_group'],
			statisticsServiceinfo: components['statistics_serviceinfo'],
		},
		data(){
			return {
				org: {},
			}
		},
		metaInfo: {
			title: '志工服務時數統計',
		},
		mounted(){
			this.tab_data = []
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

<style>

</style>