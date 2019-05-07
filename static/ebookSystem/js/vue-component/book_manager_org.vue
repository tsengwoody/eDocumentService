<template>
	<div :id="'book_manager' +org_id" class="tab-content">
		<h3>{|{ org.name }|}</h3>
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
				<button class="btn btn-default"
					@click="
						book_update = props.item;
						$refs[id].open('book_manager' +org_id);
					">資料編輯</button>
				</template>
			</table-div>
		</div>
		<modal :id_modal="id" :size="'normal'" :ref="id">
			<template slot="header">
				<h4 v-if="book_update.book_info" class="modal-title">書籍 {|{ book_update.book_info.bookname }|} 資料編輯更新</h4>
			</template>
			<template slot="body">
				<div>權重：</div>
				<select v-model="book_update.priority">
					<option
						v-for="item in '0123456789'"
						:value="item"
					>{|{ item }|}</option>
				</select>
				<div>擁有者：</div>
				<select v-model="book_update.owner">
					<option
						v-for="item in user_list"
						:value="item.id"
					>{|{ item.username }|}</option>
				</select>
			</template>
			<template slot="footer">
				<button
					class="btn btn-default"
					@click="$refs[id].close()"
				>取消</button>
				<button
					class="btn btn-default"
					@click="updates()"
				>更新</button>
			</template>
		</modal>
	</div>
</template>

<script>
	module.exports = {
		props: ['org_id',],
		components: {
			'modal': components['modal'],
			'table-div': components['table-div'],
		},
		data: function() {
			return {
				id: Math.floor(Math.random() * 100000000).toString(),
				book_update: {},
				user_list: [],
				org: {},
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
			let self = this

			this.clientg = new $.RestClient('/genericUser/api/');
			this.clientg.add('organizations');
			this.clientg.add('users');
			this.clientg.organizations.read(this.org_id)
			.done(function(data) {
				self.org = data
			})
			.fail(function(xhr, result, statusText){
				alertmessage('error', xhr.responseText)
			})
			this.clientg.users.read({role: 'guest'})
			.done(function(data) {
				self.user_list = data;
			})
			.fail(function(xhr, result, statusText){
				alertmessage('error', xhr.responseText)
			})

			this.clientb = new $.RestClient('/ebookSystem/api/');
			this.clientb.add('books');
		},
		methods: {
			search: function () {
				let self = this;
				self.book_datas = []

				self.clientb.books.read({'bookname': self.search_value, 'status': this.search_filter, 'org_id': self.org_id})
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
			updates: function () {
				let self = this
				let feedback_content = self.feedback_content
				self.clientb.books.updatepart(self.book_update.ISBN, {
					priority: self.book_update.priority,
					owner: self.book_update.owner,
				})
				.done(function(data) {
					alertmessage('success', '成功更新資料')
				})
				.fail(function(xhr, result, statusText){
					alertmessage('error', xhr.responseText)
				})

			},
		},
	}
</script>