<template>
	<div class="tab-content" style="padding:20px 0px;">
		<h2>分段管理</h2>
		<div id="ebook_manager_search">
			<div class="form-inline" style="margin-bottom:20px;">
				<div class="form-group">
					<select
						class="form-control"
						v-model="search_filter"
						id="id_search_choices" required
					>
						<option value="all" selected="selected">全部</option>
						<option v-for="(value, key) in search_choices" :value="key">{{ value }}</option>
					</select>
				</div>
				<div class="form-group">
					<input v-model="search_value" id="search_value" class="form-control" type="text" placeholder="輸入欲查詢資訊" maxlength="15">
				</div>
				<div class="form-group">
					<button type="button" class="btn btn-primary" @click="search()">搜尋</button>
				</div>
			</div>
			<table-div :header="ebook_header" :datas="ebook_datas">
				<template slot="action" slot-scope="props">
					<a
						role="button" class="btn btn-default"
						:href="'/routing/ebookSystem/ebook_review/' +props.item.ISBN_part +'/'"
						target="blank" title="(另開新視窗)"
					>審核</a>
				</template>
			</table-div>
		</div>
	</div>
</template>

<script>

	module.exports = {
		components: {
			'table-div': components['table-div'],
		},
		data(){
			return {
				search_choices: {
					'0': '未審核',
					'1': '未校對',
					'2': '校對中',
					'3': '審核校對中',
					'4': '已完成',
				},
				search_filter: 'all',
				search_value: '',
				ebook_header: {
					bookname: '文件',
					part: '段數',
					action: '動作',
				},
				ebook_datas: [],
			}
		},
		metaInfo: {
			title: '分段管理',
		},
		methods: {
			search(){
				this.ebook_datas = [];

				ebookSystemAPI.ebookRest.filter({'search': this.search_value, 'status': this.search_filter,})
				.then(res => {
					let filter_data = [];
					_.each(res.data, (v) => {
						filter_data.push({
							bookname: v.bookname,
							part: v.part,
							action: v,
						})
					})
					this.ebook_datas = filter_data;
					alertmessage('success', '查詢完成，共取得 ' +this.ebook_datas.length +' 筆資料')
				})
				.catch(res => {
					alertmessage('error', o2j(res.response.data));
				})
			},
		},
	}
</script>