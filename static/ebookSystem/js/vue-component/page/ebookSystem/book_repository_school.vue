<template>
	<div id="book_repository_school" class="container">
		<h2>平台書庫</h2>
		<div class="row">
			<div class="col-sm-3 col-md-3">
				<div class="panel-group">
					<div class="panel panel-default">
						<div class="panel-heading">
							<h4 class="panel-title">
								<span class="glyphicon glyphicon-folder-close"></span>&nbsp;&nbsp;分類列表
							</h4>
						</div>
						<div class="panel-collapse">
							<ul class="list-group">
								<li class="list-group-item" v-for="(org, index) in items">
									<a 
										v-on:click="org_read(org)"
										href='#'
									>{|{ index+1 }|}. {|{ org.name }|}</a>
									<ul>
										<li v-for="(category, index) in org.categorys">
											<a
												@click="category_read(category)"
											>{|{ category.name }|}</a>
										</li>
									</ul>
								</li>
							</ul>
						</div>
					</div>
				</div>
			</div>
			<div class="col-sm-9 col-md-9">
				<h4>{|{ pointer.name }|}書籍列表</h4>
				<bookinfo_repository :datas="books" :header="bookinfo_header"></bookinfo_repository>
			</div>
		</div>
	</div>
</template>

<script>
	module.exports = {
		props: ['org_id',],
		components: {
			'bookinfo_repository': components['bookinfo_repository'],
			'table-div': components['table-div'],
		},
		data: function(){
			return {
				user: user,
				pointer: {},
				items: [],
				orgs_books: [],
				categorys_books: [],
				books: [],
			}
		},
		computed: {
			bookinfo_header: function() {
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
			url: function(){
				return '/ebookSystem/api/categorys/';
			},
		},
		mounted: function () {
			let self = this
			document.title = '平台書庫';

			self.clientg = new $.RestClient('/genericUser/api/');
			self.clientg.add('organizations');
			self.clientb = new $.RestClient('/ebookSystem/api/');
			self.clientb.add('bookinfos');
			self.clientb.add('categorys');
			self.refresh();
		},
		methods: {
			refresh: function(){
				let self = this;

				self.items = []
				self.orgs_books = []
				self.categorys_books = []
				self.pointer = {}

				self.clientg.organizations.read()
				.done(function(data) {
					// org get category
					_.each(data, function(o){
						let org_category = {
							'id': o.id,
							'name': o.name,
							'categorys': [],
						}
						self.clientb.categorys.read({'org_id': o.id})
						.done(function(data) {
							_.each(data, function(c){
								org_category.categorys.push({
									'id': c.id,
									'name': c.name,
								})
								self.categorys_books.push({
									'id': c.id,
									'name': c.name,
								})
							})
						})
						.fail(function(xhr, result, statusText){
							alertmessage('error', xhr.responseText)
						})
						self.items.push(org_category)
						self.orgs_books.push({
							'id': o.id,
							'name': o.name,
						})
					})

					// org get book

				})
				.fail(function(xhr, result, statusText){
					alertmessage('error', xhr.responseText)
				})

			},
			category_read: function(category){
				let self = this

				self.books = []
				self.pointer = {}
				_.each(self.categorys_books, function(c){
					if(category.id===c.id){
						self.pointer = c
					}
				})

				if(!self.pointer.hasOwnProperty("id")){
					return -1
				}

				if(!self.pointer.hasOwnProperty("books")){
					self.pointer.books = []
					self.clientb.bookinfos.read({'org_id': self.pointer.id})
					.done(function(data) {
						_.each(data, function(b){
							b['action'] = b.ISBN
							self.books.push(b)
							self.pointer.books.push(b)
						})
					})
					.fail(function(xhr, result, statusText){
						alertmessage('error', xhr.responseText)
					})
				}
				else {
					_.each(self.pointer.books, function(b){
						b['action'] = b.ISBN
						self.books.push(b)
					})
				}

			},
			org_read: function(org){
				let self = this

				self.books = []
				self.pointer = {}
				_.each(self.orgs_books, function(o){
					if(org.id===o.id){
						self.pointer = o
					}
				})

				if(!self.pointer.hasOwnProperty("id")){
					return -1
				}

				if(!self.pointer.hasOwnProperty("books")){
					self.pointer.books = []
					self.clientb.bookinfos.read({'org_id': self.pointer.id})
					.done(function(data) {
						_.each(data, function(b){
							b['action'] = b.ISBN
							self.books.push(b)
							self.pointer.books.push(b)
						})
					})
					.fail(function(xhr, result, statusText){
						alertmessage('error', xhr.responseText)
					})
				}
				else {
					_.each(self.pointer.books, function(b){
						b['action'] = b.ISBN
						self.books.push(b)
					})
				}

			},
		},
	}
</script>