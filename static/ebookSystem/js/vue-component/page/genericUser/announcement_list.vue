<template>
	<div>
		<h2>公告列表</h2>
		<tab :headinglevel="3" :data="data">
			<template slot="table" slot-scope="props">
				<table-div :datas="props.item" :header="announcement_columns">
					<template slot="action" slot-scope="props">
						<a
							class="btn btn-link"
							role="button"
							:href="'/routing/genericUser/announcement/' +props.item +'/'"
						>閱讀全文</a>
					</template>
				</table-div>
			</template>
		</tab>
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
				data: [
					{
						'order': 0,
						'display_name': '平台消息',
						'value': '平台消息',
						'type': 'table',
						'data': '',
					},
					{
						'order': 1,
						'display_name': '天橋說書',
						'value': '天橋說書',
						'type': 'table',
						'data': '',
					},
					{
						'order': 2,
						'display_name': '新書推薦',
						'value': '新書推薦',
						'type': 'table',
						'data': '',
					},
					{
						'order': 3,
						'display_name': '志工快訊',
						'value': '志工快訊',
						'type': 'table',
						'data': '',
					},
				],
			}
		},
		metaInfo: {
			title: '公告列表',
		},
		mounted(){
			this.get_table_data()
		},
		methods: {
			get_table_data(){
				_.each(this.data, (v) => {
					query = {'category': v.value}

					genericUserAPI.announcementRest.filter(query)
					.then(res => {
						let filter_data = []
						_.each(res.data, (v) => {
							let temp_data = {
								"id": v.id,
								"title": v['title'],
								"datetime": v['datetime'],
								"action": v.id,
							}
							filter_data.push(temp_data)
						})
						v.data = filter_data
					})
				})
			},
		},
	}
</script>