<template>
	<div>
		<h2>平台書庫</h2>
		<ul class="nav nav-tabs">
			<li class="active"><a href="#book_repository_recommend" name="repository_books_tab_grp" data-toggle="tab" aria-expanded="true">書籍推薦</a></li>
			<li><a href="#book_repository_index" name="repository_books_tab_grp" data-toggle="tab" aria-expanded="false">索引</a></li>
			<li><a href="#book_repository_search" name="repository_books_tab_grp" data-toggle="tab" aria-expanded="false">查詢</a></li>
		</ul>

		<div class="tab-content" style="padding:20px 0px;">
			<div id="book_repository_recommend" class="tab-pane active">
				<h3 class="textfornvda">書籍推薦</h3>
				<tab :headinglevel="4" :data="recommend_data">
					<template slot="bookinfo_repository" slot-scope="props">
						<bookinfo_repository :datas="props.item.datas" :header="props.item.header"></bookinfo_repository>
					</template>
				</tab>
			</div>
			<div id="book_repository_index" class="tab-pane fade">
				<h3 class="textfornvda">索引</h3>
				<tab :headinglevel="4" :data="index_data">
					<template slot="bookinfo_repository" slot-scope="props">
						<bookinfo_repository :datas="props.item.datas" :header="props.item.header"></bookinfo_repository>
					</template>
				</tab>
			</div>
			<div id="book_repository_search" class="tab-pane fade">
				<h3 class="textfornvda">查詢</h3>
				<div class="form-inline" style="margin-bottom:20px;">
					<div class="form-group">
						<input v-model="search_value" id="search_value" class="form-control" type="text" placeholder="輸入欲查詢資訊" maxlength="15">
					</div>
					<div class="form-group">
						<button type="button" class="btn btn-primary" @click="search()">搜尋</button>
					</div>
				</div>
				<bookinfo_repository :datas="bookinfos.datas" :header="bookinfos.header"></bookinfo_repository>
			</div>
		</div>
	</div>
</template>

<script>
	// TODO: 這邊的 user 是全域變數，之後可能會改

	module.exports = {
		components: {
			'tab': components['tab'],
			'bookinfo_repository': components['bookinfo_repository'],
		},
		data(){
			return {
				user: user,	
				recommend_data: [
					{
						order: 0,
						display_name: '最新上架',
						value: 'newest',
						type: 'bookinfo_repository',
						data: '',
					},
					{
						order: 1,
						display_name: '平台推薦',
						value: 'recommend',
						type: 'bookinfo_repository',
						data: '',
					},
					{
						order: 2,
						display_name: '借閱排行',
						value: 'hottest',
						type: 'bookinfo_repository',
						data: '',
					},
				],
				index_data: [
					{
						'order': 0,
						'display_name': '總類',
						'value': '0',
						'type': 'bookinfo_repository',
						'data': '',
					},
					{
						'order': 1,
						'display_name': '哲學',
						'value': '1',
						'type': 'bookinfo_repository',
						'data': '',
					},
					{
						'order': 2,
						'display_name': '宗教',
						'value': '2',
						'type': 'bookinfo_repository',
						'data': '',
					},
					{
						'order': 3,
						'display_name': '科學',
						'value': '3',
						'type': 'bookinfo_repository',
						'data': '',
					},
					{
						'order': 4,
						'display_name': '應用科學',
						'value': '4',
						'type': 'bookinfo_repository',
						'data': '',
					},
					{
						'order': 5,
						'display_name': '社會科學',
						'value': '5',
						'type': 'bookinfo_repository',
						'data': '',
					},
					{
						'order': 6,
						'display_name': '史地類',
						'value': '6',
						'type': 'bookinfo_repository',
						'data': '',
					},
					{
						'order': 7,
						'display_name': '世界史地',
						'value': '7',
						'type': 'bookinfo_repository',
						'data': '',
					},
					{
						'order': 8,
						'display_name': '語言文學',
						'value': '8',
						'type': 'bookinfo_repository',
						'data': '',
					},
					{
						'order': 9,
						'display_name': '藝術',
						'value': '9',
						'type': 'bookinfo_repository',
						'data': '',
					},
				],
				search_value: '',
				bookinfos: '',
			}
		},
		computed: {
			bookinfo_columns(){
				if(this.user.auth_guest){
					return {
						ISBN: "ISBN",
						bookname: "書名",
						bookbinding: "裝訂冊數",
						order: "版次",
						author: "作者",
						house: "出版社",
						date: "出版日期",
						action: "動作",
					}
				} else {
					return {
						ISBN: "ISBN",
						bookname: "書名",
						bookbinding: "裝訂冊數",
						order: "版次",
						author: "作者",
						house: "出版社",
						date: "出版日期",
					}
				}
			},
		},
		metaInfo: {
			title: '平台書庫',
		},
		mounted: function () {
			this.get_recommend_table_data();
			this.get_index_table_data();
		},
		methods: {
			get_recommend_table_data(){
				_.each(this.recommend_data, (v) => {
					let query = {};
					query[v.value] = 30;
					ebookSystemAPI.bookInfoRest.filter(query)
					.then(res => {
						let filter_data = [];
						_.each(res.data, (o) => {
							filter_data.push({
								ISBN: o['ISBN'],
								bookname: o['bookname'],
								bookbinding: o['bookbinding'],
								order: o['order'],
								author: o['author'],
								house: o['house'],
								date: o['date'],
								action: o['ISBN'],
							})
						})
						v.data = {};
						v.data['header'] = this.bookinfo_columns;
						v.data['datas'] = filter_data;
					})
					.catch(res => {
						alertmessage('error', o2j(res.response.data));
					})
				})
			},
			get_index_table_data(){
				_.each(this.index_data, (v) => {
					const query = {'chinese_book_category': v.value};
					ebookSystemAPI.bookInfoRest.filter(query)
					.then(res => {
						let filter_data = [];
						_.each(res.data, (o) => {
							filter_data.push({
								ISBN: o['ISBN'],
								bookname: o['bookname'],
								bookbinding: o['bookbinding'],
								order: o['order'],
								author: o['author'],
								house: o['house'],
								date: o['date'],
								action: o['ISBN'],
							})
						})
						v.data = {};
						v.data['header'] = this.bookinfo_columns;
						v.data['datas'] = filter_data;
					})
				})
			},
			search(){
				const query = {'search': this.search_value};
				ebookSystemAPI.bookInfoRest.filter(query)
				.then(res => {
					let filter_data = [];
					_.each(res.data, function(o) {
						filter_data.push({
							ISBN: o['ISBN'],
							bookname: o['bookname'],
							bookbinding: o['bookbinding'],
							order: o['order'],
							author: o['author'],
							house: o['house'],
							date: o['date'],
							action: o['ISBN'],
						})
					})
					this.bookinfos = {};
					this.bookinfos['header'] = this.bookinfo_columns;
					this.bookinfos['datas'] = filter_data;
					alertmessage('success', '查詢完成，共取得 ' +this.bookinfos.datas.length +' 筆資料')
				})
				.catch(res => {
					alertmessage('error', o2j(res.response.data));
				})

			},
		},
	}
</script>
