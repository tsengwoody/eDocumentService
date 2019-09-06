<template>
	<div>
		<h2>志工服務時數統計</h2>
		<panel-group :data="tab_data" :title="'單位'">
			<template slot="statistics_serviceinfo" slot-scope="props">
				<statistics-serviceinfo
					:org="props.item"
				></statistics-serviceinfo>
			</template>
		</panel-group>
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
				tab_data: [],
			}
		},
		metaInfo: {
			title: '志工服務時數統計',
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