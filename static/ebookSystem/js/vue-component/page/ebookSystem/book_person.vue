<template>
	<div id="book_person">
		<h2>校對進度</h2>
		<tab :headinglevel="3" :data="data">
			<template slot="table" slot-scope="props">
				<table-div :datas="props.item.datas" :header="props.item.header">
					<template slot="inactive_book_action" slot-scope="props">
						<a v-if="user.is_manager" class="btn btn-default" role="button" :href="'/routing/ebookSystem/book_review/' +props.item.ISBN +'/'" target="_blank" title="審核(另開新視窗)">審核</a>
						<button class="btn btn-default" @click="book_del(props.item.ISBN)">刪除</button>
					</template>
					<template slot="active_book_action" slot-scope="props">
						<button
							class="btn btn-default send_button"
							@click="
							$refs['sp_instance'].instance_set(props.item.ISBN);
							$refs['spm_instance'].open('book_person');
						">設定權重</button>
						<a class="btn btn-default" :href="'/routing/ebookSystem/book_detail/' +props.item.ISBN +'/'" target="_blank" title="分段資訊(另開新視窗)">分段資訊</a>
					</template>
				</table-div>
			</template>
			<template slot="bookinfo_repository_table" slot-scope="props">
				<bookinfo_repository :datas="props.item.datas" :header="props.item.header"></bookinfo_repository>
			</template>
		</tab>
		<modal :id_modal="'spm'" ref="spm_instance">
			<template slot="header">
				<h4 class="modal-title">權重設定</h4>
			</template>   
			<template slot="body">
				<div class="text-center">*權重設定，最高: 1，最低: 9</div>
				<div class="form-horizontal">
					<set_priority
						ref="sp_instance"
						v-on:update="
							get_table_data();
							$refs['spm_instance'].close();
					"></set_priority>
				</div>
			</template>
			<template slot="footer">
				<button class="btn btn-default"
					@click="$refs.sp_instance.set_priority()"
				>送出</button>
			</template>
		</modal>
	</div>
</template>

<script>
	module.exports = {
		components: {
			'table-div': components['table-div'],
			'tab': components['tab'],
			'modal': components['modal'],
			'bookinfo_repository': components['bookinfo_repository'],
			'set_priority': components['set_priority'],
		},
		data(){
			return {
				bookinfo_header: {
					"ISBN": "ISBN",
					"bookname": "書名",
					"bookbinding": "裝訂冊數",
					"order": "版次",
					"author": "作者",
					"house": "出版社",
					"date": "出版日期",
					"action": "動作",
				},
				active_book_header: {
					"ISBN": "ISBN",
					"bookname": "書名",
					"page": "頁數/總頁數",
					"finish_part_count": "已完成段數",
					"service_hours": "時數",
					"priority": "權重",
					"active_book_action": "動作",
				},
				inactive_book_header: {
					"ISBN": "ISBN",
					"bookname": "書名",
					"owner": "上傳者",
					"upload_date": "上傳日期",
					"inactive_book_action": "動作",
				},
				data: [
					{
						'order': 0,
						'display_name': '已校對',
						'value': 'finish',
						'type': 'bookinfo_repository_table',
						'data': '',
					},
					{
						'order': 1,
						'display_name': '校對中',
						'value': 'active',
						'type': 'table',
						'data': '',
					},
					{
						'order': 2,
						'display_name': '未審核',
						'value': 'inactive',
						'type': 'table',
						'data': '',
					},
				],
			}
		},
		metaInfo: {
			title: '校對進度',
		},
		mounted(){
			this.get_table_data();
		},
		methods: {
			get_table_data(){
				//finish book
				let query = {'owner_id': user.id};
				ebookSystemAPI.bookInfoRest.filter(query)
				.then(res => {
					let filter_data = []
					_.each(res.data, (v) => {
						filter_data.push({
							"ISBN": v['ISBN'],
							"bookname": v['bookname'],
							"bookbinding": v['bookbinding'],
							"order": v['order'],
							"author": v['author'],
							"house": v['house'],
							"date": v['date'],
							"action": v['ISBN'],
						})
					})
					this.data[0].data = {};
					this.data[0].data['header'] = this.bookinfo_header;
					this.data[0].data['datas'] = filter_data;
				})

				//active book
				const c1 = ebookSystemAPI.bookRest.filter({'status': 1, 'owner_id': user.id});
				const c2 = ebookSystemAPI.bookRest.filter({'status': 2, 'owner_id': user.id});
				Promise.all([c1, c2])
				.then(res => {
					let book_data = [];
					book_data = book_data.concat(res[0].data);
					book_data = book_data.concat(res[1].data);
					let filter_data = [];
					_.each(book_data, (v) => {
						filter_data.push({
							"ISBN": v.book_info.ISBN,
							"bookname": v.book_info.bookname,
							"page": v.finish_page_count.toString() +'/' +v.page_count.toString(),
							"finish_part_count": v.finish_part_count,
							"service_hours": v.service_hours,
							"priority": v.priority,
							"active_book_action": v,
						})
					})
					this.data[1].data = {};
					this.data[1].data['header'] = this.active_book_header;
					this.data[1].data['datas'] = filter_data;
				})

				//inactive book
				query = {'status': 0, 'owner_id': user.id};
				ebookSystemAPI.bookRest.filter(query)
				.then(res => {
					let filter_data = [];
					_.each(res.data, (v) => {
						filter_data.push({
							"ISBN": v.book_info.ISBN,
							"bookname": v.book_info.bookname,
							"owner": v.owner,
							"upload_date": v.upload_date,
							"inactive_book_action": v,
						})
					});
					this.data[2].data = {};
					this.data[2].data['header'] = this.inactive_book_header;
					this.data[2].data['datas'] = filter_data;
				})

			},
			book_del(pk){
				alertconfirm('確認刪除書籍 id:' +pk)
				.done(() => {
					ebookSystemAPI.bookRest.delete(pk)
					.then(res => {
						alertmessage('success', '成功刪除書籍 id:' +pk)
						this.get_table_data();
					})
					.catch(res => {
						alertmessage('error', o2j(res.response.data));
					})
				})
			},
		},
	}
</script>
