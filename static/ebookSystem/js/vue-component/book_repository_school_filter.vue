<template>
	<div class="book_repository_school_filter">
		<h3 class="textfornvda">查詢</h3>
		<div class="form-horizontal">
			<div class="form-group">
				<label class="control-label col-sm-2" for="id_search_ISBN">單位:</label>
				<div class="col-sm-3">
					<select
						class="form-control"
						v-model="search_org_id"
						placeholder="請選擇單位"
					>
						<option value="0" selected>全部</option>
						<option v-for="org in organizations" :key="org.id" :value="org.id">{|{ org.name }|}</option>
					</select>
				</div>
			</div>

			<div class="form-group">
				<label class="control-label col-sm-2" for="id_search_ISBN">類別:</label>
				<div class="col-sm-3">
					<select
						v-if="selected_org"
						class="form-control"
						v-model="search_category_id"
						name="category"
						placeholder="請選擇類別"
					>
						<option value="all" selected="selected">全部</option>
						<option
							v-for="category in selected_org.categorys"
							:key="category.id"
							:value="category.id"
						>{|{ category.name }|}</option>
					</select>
					<select
						v-else
						class="form-control"
						disabled
					>
						<option value="all" selected="selected">全部</option>
					</select>
				</div>
			</div> 

			<div class="form-group">
				<label class="control-label col-sm-2" for="id_search_ISBN">關鍵字:</label>
				<div class="col-sm-3">
					<input v-model="search_value" id="search_value" class="form-control" type="text" placeholder="輸入欲查詢資訊" maxlength="15">
				</div>
			</div>

			<div class="form-group">
				<div class="col-sm-3 col-sm-offset-2">
					<button type="button" class="btn btn-primary" @click="search">搜尋</button>
					<span class="book_search_result">共查到 {|{ bookinfosData.length }|} 筆資料</span>
				</div>
			</div>
		</div>

		<bookinfo_repository :datas="bookinfosData" :header="bookinfo_header"></bookinfo_repository>
	</div>
</template>

<script>
	module.exports = {
		props: ['organizations', ],
		components: {
			'bookinfo_repository': components['bookinfo_repository'],
		},
		data(){
			return {
				user: user,
				search_value: '',
				bookinfosData: [],
				organizations: [],
				search_category_id: 'all',
				search_org_id: '0',
			}
		},
		computed: {
			bookinfo_header() {
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
			selected_org() {
				if (this.search_org_id) {
					return this.organizations.find(org => org.id === this.search_org_id);
				}
				return null;
			}
		},
		methods: {
			search() {
				let query = {search: this.search_value};
				if(!(this.search_org_id=='0')){
					query['org_id'] = this.search_org_id;
				}
				if(!(this.search_category_id=='all')){
					query['category_id'] = this.search_category_id;
				}
				if(String(this.search_category_id).endsWith('null')){
					query['category_id'] = 'null';
				}
				console.log(query)
				ebookSystemAPI.bookInfoRest.filter(query)
				.then(res => {
					this.bookinfosData = [];
					_.each(res.data, (o) => {
						this.bookinfosData.push({
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
					alertmessage('success', '查詢完成，共取得 ' +this.bookinfosData.length +' 筆資料')
				})
				.catch(res => {
					alertmessage('error', o2j(res.response.data));
				})

			},
		},
	}
</script>

<style>
	
</style>