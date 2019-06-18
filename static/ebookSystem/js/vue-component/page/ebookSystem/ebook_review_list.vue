<template>
	<div>
		<h2>校對文件審核</h2>
		<panel_group :data="tab_data" :title="'單位'">
			<template slot="ebook_review_list_org" slot-scope="props">
				<ebook_review_list_org :org_id="props.item">
				</ebook_review_list_org>
			</template>
		</panel_group>
	</div>
</template>

<script>
	module.exports = {
		components: {
			'ebook_review_list_org': components['ebook_review_list_org'],
			'panel_group': components['panel_group'],
		},
		data: function() {
			return {
				tab_data: [],
			}
		},
		metaInfo: {
			title: '校對文件審核',
		},
		mounted: function () {
			this.tab_data = []
			genericUserAPI.organizationRest.list()
			.then(res => {
				_.each(res.data, (v) => {
					this.tab_data.push({
						'order': v.id,
						'display_name': v.name,
						'value': v.id,
						'type': 'ebook_review_list_org',
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