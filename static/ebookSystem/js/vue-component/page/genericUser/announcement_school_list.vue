<template>
	<div>
		<h2>校園公告列表</h2>

		<table-div
			:datas="announcement_datas"
			:header="announcement_columns"
		>
			<template slot="action" slot-scope="props">
				<a
					class="btn btn-link"
					role="button"
					:href="'/routing/genericUser/announcement/' +props.item +'/'"
				>閱讀全文</a>
			</template>
		</table-div>

	</div>
</template>

<script>
	module.exports = {
		components: {
			'bookinfo_repository': components['bookinfo_repository'],
			'tab': components['tab'],
			'table-div': components['table-div'],
		},
		data(){
			return {
				announcement_columns: {
					'title': '標題',
					'datetime': '發佈日期',
					'action': '動作',
				},
				announcement_datas: [],
			}
		},
		metaInfo: {
			title: '校園公告列表',
		},
		mounted(){
			this.get_table_data()
		},
		methods: {
			get_table_data(){

				query = {'category': '校園公告'}

				genericUserAPI.announcementRest.filter(query)
				.then((response) => {
					let filter_data = []
					_.each(response.data, (v) => {
						let temp_data = {
							"id": v.id,
							"title": v['title'],
							"datetime": v['datetime'],
							"action": v.id,
						}
						filter_data.push(temp_data)
					})
					this.announcement_datas = filter_data
				})

			},
		},
	}
</script>