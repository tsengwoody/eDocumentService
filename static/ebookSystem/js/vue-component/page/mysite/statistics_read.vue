<template>
	<div>
		<h2>視障者閱讀統計</h2>
		<panel-group :data="tab_data" :title="'單位'">
			<template slot="statistics_serviceinfo" slot-scope="props">
				<statistics-read
					:org="props.item"
				></statistics-read>
			</template>
		</panel-group>
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
				tab_data: [],
			}
		},
		metaInfo: {
			title: '視障者閱讀統計',
		},
		mounted(){
			this.tab_data = []
			genericUserAPI.organizationRest.list()
			.then(res => {
				_.each(res.data, (v) => {
					this.tab_data.push({
						'order': v.id,
						'display_name': v.name,
						'value': v.id,
						'type': 'statistics_serviceinfo',
						'data': v,
					})
				})
			})
			.catch(res => {
				alertmessage('error', o2j(res.response.data));
			})
		},
	}
</script>

<style>

</style>