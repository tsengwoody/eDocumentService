<template>
	<div>
		<h2>服務時數確認</h2>
		<panel_group :data="tab_data" :title="'單位'">
			<template slot="serviceinfo_list_check_org" slot-scope="props">
				<serviceinfo_list_check_org :org_id="props.item">
				</serviceinfo_list_check_org>
			</template>
		</panel_group>
	</div>
</template>

<script>
	module.exports = {
		components: {
			'serviceinfo_list_check_org': components['serviceinfo_list_check_org'],
			'panel_group': components['panel_group'],
		},
		data(){
			return {
				tab_data: [],
			}
		},
		metaInfo: {
			title: '服務時數確認',
		},
		mounted(){
			genericUserAPI.organizationRest.list()
			.then(res => {
				_.each(res.data, (v)=> {
					this.tab_data.push({
						'order': v.id,
						'display_name': v.name,
						'value': v.id,
						'type': 'serviceinfo_list_check_org',
						'data': v.id,
					})
				})
			})
			.catch(res => {
				alertmessage('error', o2j(res.response.data));
			})
		},
	}
</script>