<template>
	<div :id="'book_manager' +org_id" class="tab-content">
		<h3>{{ org.name }}</h3>
		<div id="book_manager_search">
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
				<h4 v-if="book_update.book_info" class="modal-title">書籍 {{ book_update.book_info.bookname }} 資料編輯更新</h4>
			</template>
			<template slot="body">
				<div class="form-group col-md-6">
					<label for="priority">權重：</label>
					<select class="form-control" id="priority"
						 v-model="book_update.priority"
					>
					    <option
							v-for="item in '0123456789'"
							:value="item"
						>{{ item }}</option>
				    </select>
				</div>

				<div class="form-group col-md-6">
					<label for="owner">擁有者：</label>
					<select class="form-control" id="owner"
						 v-model="book_update.owner"
					>
				      	<option
							v-for="item in user_list"
							:value="item.id"
						>{{ item.username }}</option>
				    </select>
				</div>

				<div style="clear: both;"></div>
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
		data(){
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
		mounted(){
			genericUserAPI.organizationRest.read(this.org_id)
			.then(res => {
				this.org = res.data
			})
			.catch(res => {
				alertmessage('error', o2j(res.response.data));
			})

			genericUserAPI.userRest.filter({role: 'guest'})
			.then(res => {
				this.user_list = res.data;
			})
			.catch(res => {
				alertmessage('error', o2j(res.response.data));
			})
		},
		methods: {
			search(){
				ebookSystemAPI.bookRest.filter({'bookname': this.search_value, 'status': this.search_filter, 'org_id': this.org_id})
				.then(res => {
					this.book_datas = [];
					_.each(res.data, (v) => {
						this.book_datas.push({
							'ISBN': v.ISBN,
							'bookname': v.book_info.bookname,
							'page': v.finish_page_count +'/' +v.page_count,
							'finish_part_count': v.finish_part_count,
							'service_hours': v.service_hours,
							'action': v,
						})
					})
					alertmessage('success', '查詢完成，共取得 ' +this.book_datas.length +' 筆資料')
				})
				.catch(res => {
					alertmessage('error', o2j(res.response.data));
				})
			},
			updates(){
				let feedback_content = this.feedback_content
				ebookSystemAPI.bookSimpleRest.partialupdate(this.book_update.ISBN, {
					priority: this.book_update.priority,
					owner: this.book_update.owner,
				})
				.then(res => {
					alertmessage('success', '成功更新資料')
				})
				.catch(res => {
					alertmessage('error', o2j(res.response.data));
				})
			},
		},
	}
</script>