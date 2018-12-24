<template>
	<div class="tab-content" style="padding:20px 0px;">
		<h2>書籍管理</h2>
		<div id="book_manager_search">
			<div class="form-inline" style="margin-bottom:20px;">
				<div class="form-group">
					<select
						class="form-control"
						v-model="search_filter"
						id="id_search_choices" required
					>
						<option value="all" selected="selected">全部</option>
						<option v-for="(value, key) in search_choices" :value="key">{|{ value }|}</option>
					</select>
				</div>
				<div class="form-group">
					<input v-model="search_value" id="search_value" class="form-control" type="text" placeholder="輸入欲查詢資訊" maxlength="15">
				</div>
				<div class="form-group">
					<button type="button" class="btn btn-primary" @click="search()">搜尋</button>
				</div>
			</div>
			<table-div :header="book_header" :datas="book_datas">
				<template slot="action" slot-scope="props">
					<a
						role="button" class="btn btn-default"
						:href="'/routing/ebookSystem/book_review/' +props.item.ISBN +'/'"
						target="blank" title="(另開新視窗)"
					>審核</a>
					<a
						role="button" class="btn btn-default"
						:href="'/routing/ebookSystem/book_detail/' +props.item.ISBN +'/'"
						target="blank" title="(另開新視窗)"
					>分段資訊</a>
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
		data: function() {
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
				book_header: {
					'ISBN': 'ISBN',
					'bookname': '書名',
					'page': '頁數/總頁數',
					'finish_part_count': '已完成段數',
					'service_hours': '時數',
					'action': '動作',
				},
				book_datas: [],
			}
		},
		mounted: function () {
			document.title = '書籍管理';
			this.client = new $.RestClient('/ebookSystem/api/');
			this.client.add('books');
			this.client.add('bookadds');
		},
		methods: {
			search: function () {
				let self = this;
				self.book_datas = []

				self.client.books.read({'bookname': self.search_value, 'status': this.search_filter,})
				.done(function(data) {
					filter_data = []
					_.each(data, function(v){
						filter_data.push({
							'ISBN': v.ISBN,
							'bookname': v.book_info.bookname,
							'page': v.finish_page_count +'/' +v.page_count,
							'finish_part_count': v.finish_part_count,
							'service_hours': v.service_hours,
							'action': v,
						})
					})
					self.book_datas = filter_data,

					alertmessage('success', '查詢完成，共取得 ' +self.book_datas.length +' 筆資料')
				})
				.fail(function(xhr, result, statusText){
					alertmessage('error', xhr.responseText)
				})
			},
		},
	}
</script>
