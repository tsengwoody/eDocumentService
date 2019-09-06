<template>
	<div id="book_repository_school" class="container">
		<h2>平台書庫
			<span class="heading-btns">
				<button class="btn btn-default" v-if="!isSearch" @click="isSearch = true">進入書籍查尋</button>
				<button class="btn btn-default" v-if="isSearch" @click="isSearch = false">進入書籍索引</button>
			</span>
		</h2>
		<div class="row" v-if="!isSearch">
			<div class="col-sm-3 col-md-3">
				<div class="panel-group">
					<div class="panel panel-default">
						<div class="panel-heading">
							<h3 class="panel-title">
								<span class="glyphicon glyphicon-folder-close"></span>&nbsp;&nbsp;分類列表
							</h3>
						</div>
						<div class="panel-collapse">
							<ul class="list-group">
								<li class="list-group-item" v-for="(org, index) in items">
									<a 
										@click="org_read(org)"
										href='#'
									>
										<i class="fa fa-chevron-down" aria-hidden="true" 
											v-if="selected_org === org.id"
										></i>
										<i class="fa fa-chevron-right" aria-hidden="true" v-else></i>
										&nbsp;{{ org.name }}
									</a>
									<transition name="fade">
										<ol style="list-style-image:none;" v-if="selected_org === org.id">
											<li style="margin-top: 0.5em; cursor: pointer;" v-for="(category, index) in org.categorys">
												<a
													@click="category_read(category)"
												>{{ category.name }}</a>
											</li>
										</ol>
									</transition>
								</li>
							</ul>
						</div>
					</div>
				</div>
			</div>
			<div class="col-sm-9 col-md-9">
				<h3>{{ pointer.name }}書籍列表</h3>
				<bookinfo_repository :datas="books" :header="bookinfo_header"></bookinfo_repository>
			</div>
		</div>

		<template v-else>
			<book_repository_school_filter :organizations="items"></book_repository_school_filter>
		</template>
	</div>
</template>

<script>
	module.exports = {
		props: ['org_id',],
		components: {
			'bookinfo_repository': components['bookinfo_repository'],
			'book_repository_school_filter': components['book_repository_school_filter'],
		},
		data(){
			return {
				user: user,
				selected_org: null,
				pointer: {},
				items: [],
				orgs_books: [],
				categorys_books: [],
				books: [],
				isSearch: false,
			}
		},
		computed: {
			bookinfo_header(){
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
		mounted(){
			this.refresh();
		},
		methods: {
			refresh: function() {
				this.items = []
				this.orgs_books = []
				this.categorys_books = []
				this.pointer = {}

				genericUserAPI.organizationRest.list()
				.then(res => {
					// org get category
					_.each(res.data, (o) => {
						// org 為 1 屬特殊情形，是一般版使用，故在選擇列表內不顯示
						if(0 && o.id==1){
							return -1;
						}
						let org_category = {
							'id': o.id,
							'name': o.name,
							'categorys': [],
						}

						let temp = {
							'id': o.id +'-null',
							'name': '未分類',
						}

						org_category.categorys.push(temp)
						this.categorys_books.push(temp)

						ebookSystemAPI.categoryRest.filter({'org_id': o.id})
						.then(res => {
							_.each(res.data, (c) => {
								let temp = {
									'id': c.id,
									'name': c.name,
								}
								org_category.categorys.push(temp)
								this.categorys_books.push(temp)
							})
						})
						.catch(res => {
							alertmessage('error', o2j(res.response.data));
						})
						this.items.push(org_category)
						this.orgs_books.push({
							'id': o.id,
							'name': o.name,
						})
					})

				})
				.catch(res => {
					alertmessage('error', o2j(res.response.data));
				})

			},
			category_read(category){
				this.books = [];
				this.pointer = {};
				_.each(this.categorys_books, (c) => {
					if(category.id===c.id){
						this.pointer = c;
					}
				})

				if(!this.pointer.hasOwnProperty("id")){
					return -1;
				}

				if(!this.pointer.hasOwnProperty("books")){
					let param = {};

					try {
						if( this.pointer.id.endsWith('null') && (this.pointer.id.split('-').length===2) ){
							let org_id = this.pointer.id.split('-')[0];
							let category_id = this.pointer.id.split('-')[1];
							param = {'org_id': org_id, 'category_id': category_id};
						}
						else{
							param = {'category_id': this.pointer.id};
						}
					}
					catch (err) {
						param = {'category_id': this.pointer.id};
					}

					this.pointer.books = [];
					ebookSystemAPI.bookInfoRest.filter(param)
					.then(res => {
						_.each(res.data, (b) => {
							b['action'] = b.ISBN;
							this.books.push(b);
							this.pointer.books.push(b);
						})
					})
					.catch(res => {
						alertmessage('error', o2j(res.response.data));
					})
				}
				else {
					_.each(this.pointer.books, (b) => {
						b['action'] = b.ISBN
						this.books.push(b)
					})
				}

			},
			org_read(org) {
				if (this.selected_org === org.id) {
					this.selected_org = null;
				} else {
					this.selected_org = org.id;
				}

				this.books = [];
				this.pointer = {};
				_.each(this.orgs_books, (o) => {
					if(org.id===o.id){
						this.pointer = o;
					}
				})

				if(!this.pointer.hasOwnProperty("id")){
					return -1;
				}

				if(!this.pointer.hasOwnProperty("books")){
					this.pointer.books = [];
					ebookSystemAPI.bookInfoRest.filter({'org_id': this.pointer.id})
					.then(res => {
						_.each(res.data, (b) => {
							b['action'] = b.ISBN;
							this.books.push(b);
							this.pointer.books.push(b);
						})
					})
					.catch(res => {
						alertmessage('error', o2j(res.response.data));
					})
				}
				else {
					_.each(this.pointer.books, (b) => {
						b['action'] = b.ISBN;
						this.books.push(b);
					})
				}

			},
		},
	}
</script>

<style>
.fade-enter-active, .fade-leave-active {
  transition: opacity .5s;
}

.fade-leave-active {
  transition: opacity .1s;
}
.fade-enter, .fade-leave-to {
  opacity: 0;
}

.heading-btns {
	margin-left: 1.5rem;
}
</style>