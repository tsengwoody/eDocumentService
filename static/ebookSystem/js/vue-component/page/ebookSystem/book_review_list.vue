<template>
	<div>
		<h2>上傳文件審核</h2>
		<panel_group :data="tab_data" :title="'單位'">
			<template slot="book_review_list_org" slot-scope="props">
				<book_review_list_org :org_id="props.item">
				</book_review_list_org>
			</template>
		</panel_group>
	</div>
</template>

<script>
	module.exports = {
		components: {
			'book_review_list_org': components['book_review_list_org'],
			'panel_group': components['panel_group'],
		},
		data: function() {
			return {
				tab_data: [],
			}
		},
		metaInfo: {
			title: '上傳文件審核',
		},
		mounted(){
			this.tab_data = [];
			genericUserAPI.organizationRest.list()
			.then(res => {
				_.each(res.data, (v) => {
					this.tab_data.push({
						'order': v.id,
						'display_name': v.name,
						'value': v.id,
						'type': 'book_review_list_org',
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