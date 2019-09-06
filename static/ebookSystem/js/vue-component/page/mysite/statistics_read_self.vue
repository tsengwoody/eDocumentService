<template>
	<div>
		<h2>視障者閱讀統計</h2>
			<statistics-read
				:org="org"
			></statistics-read>
		</template>
	</div>
</template>

<script>
	module.exports = {
		components: {
			panelGroup: components['panel_group'],
			statisticsRead: components['statistics_read'],
		},
		data(){
			return {
				org: {},
			}
		},
		metaInfo: {
			title: '視障者閱讀統計',
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