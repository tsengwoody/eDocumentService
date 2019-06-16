<template>
	<div>
		<h2>使用者管理</h2>
		<panel_group :data="tab_data" :title="'單位'">
			<template slot="user_manager_org" slot-scope="props">
				<user_manager_org :org_id="props.item">
				</user_manager_org>
			</template>
		</panel_group>
	</div>
</template>

<script>
	module.exports = {
		components: {
			'user_manager_org': components['user_manager_org'],
			'panel_group': components['panel_group'],
		},
		data(){
			return {
				tab_data: [],
			}
		},
		metaInfo: {
			title: '使用者管理',
		},
		mounted(){
			genericUserAPI.organizationRest.list()
			.then(res => {
				_.each(res.data, (v) => {
					this.tab_data = []
					this.tab_data.push({
						'order': v.id,
						'display_name': v.name,
						'value': v.id,
						'type': 'user_manager_org',
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