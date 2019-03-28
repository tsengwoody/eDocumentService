<template>
	<div :id="'category_manager' +org_id" class="container">
		<h3>{|{ org.name }|}</h3>
		<div class="row">
			<div class="col-sm-3 col-md-3">
				<div class="panel-group">
					<div class="panel panel-default">
						<div class="panel-heading">
							<h4 class="panel-title">
								<span class="glyphicon glyphicon-folder-close"></span>&nbsp;&nbsp;分類列表
							</h4>
							<button
								class="btn btn-default"
								@click="
									$refs['cc' +org_id].open('category_manager' +org_id);
								"
							>新增</button>
						</div>
						<div class="panel-collapse">
							<ul class="list-group">
								<li class="list-group-item" v-for="(item, index) in items">
									<a 
										@click="pointer=item"
										href='#'
									>{|{ index+1 }|}. {|{ item.name }|}</a>

									<span v-if="index > 0">
										<i class="fa fa-pencil-square-o"
											role="button"
											title="更名" 
											@click="
												category_id = item.id;
												category_name = item.name;
												$refs['cu' +org_id].open('category_manager' +org_id);
											"
										></i>

										<i class="fa fa-times"
											role="button"
											title="刪除" 
											@click="category_delete(item)"
											style="font-size: 1.2em;" 
										></i>
									</span>
								</li>
							</ul>
						</div>
					</div>
				</div>
			</div>
			<div class="col-sm-9 col-md-9">
				<div
					v-for="(item, index) in items"
					v-if="pointer.id===item.id"
				>
					<h4>{|{ item.name }|}書籍列表</h4>
					<table-div :datas="item.book_list" :header="bookinfo_columns">
						<template slot="action" slot-scope="props">
							<button
								class="btn btn-default"
								@click="
									book_ISBN = props.item;
									book_category_id=pointer.id;
									$refs['bcu' +org_id].open('category_manager' +org_id);
								"
							>變更</button>
						</template>
					</table-div>
				</div>
			</div>
		</div>
		<modal :id_modal="'bcu' +org_id" :size="'normal'" :ref="'bcu' +org_id">
			<template slot="header">
				<h4 class="modal-title">書籍{|{ book_ISBN }|}類別變更</h4>
			</template>
			<template slot="body">
				<div class="form-horizontal">
					<form-drf 
						:model_info="model_info.book_category_id"
						:input-class="'col-sm-6'"
						:offset-class="'col-sm-offset-1'"
						:field="'book_category_id'"
						v-model="book_category_id"
						@keyup.enter.native="book_category_update()"
					></form-drf>
				</div>
			</template>
			<template slot="footer">
				<button
					class="btn btn-default"
					@click="book_category_update();"
				>變更</button>
			</template>
		</modal>
		<modal :id_modal="'cc' +org_id" :size="'normal'" :ref="'cc' +org_id">
			<template slot="header">
				<h4 class="modal-title">類別新增</h4>
			</template>
			<template slot="body">
				<div class="form-horizontal">
					<form-drf 
						:model_info="model_info.category_name"
						:input-class="'col-sm-6'"
						:offset-class="'col-sm-offset-1'"
						:field="'category_name'"
						v-model="category_name"
						@keyup.enter.native="category_create();"
					></form-drf>
				</div>
			</template>
			<template slot="footer">
				<button
					class="btn btn-default"
					@click="category_create();"
				>新增</button>
			</template>
		</modal>
		<modal :id_modal="'cu' +org_id" :size="'normal'" :ref="'cu' +org_id">
			<template slot="header">
				<h4 class="modal-title">類別{|{ category_id }|}更名</h4>
			</template>
			<template slot="body">
				<div class="form-horizontal">
					<form-drf 
						:model_info="model_info.category_name"
						:input-class="'col-sm-6'"
						:offset-class="'col-sm-offset-1'"
						:field="'category_name'"
						v-model="category_name"
						@keyup.enter.native="category_update();"
					></form-drf>
				</div>
			</template>
			<template slot="footer">
				<button
					class="btn btn-default"
					@click="category_update();"
				>變更</button>
			</template>
		</modal>
	</div>
</template>

<script>
	module.exports = {
		props: ['org_id',],
		components: {
			'form-drf': components['form'],
			'modal': components['modal'],
			'tab': components['tab'],
			'table-div': components['table-div'],
		},
		data: function(){
			return {
				user: user,
				org: {},
				pointer: {},
				items: [
					{
						'id': 0,
						'name': '未分類',
						'book_list': [],
					},
				],
				book_ISBN: '', // use in bcu modal pointer
				book_category_id: 0, // use in bcu modal input
				category_id: '', // use in cu modal pointer
				category_name: '', // use in cu modal input
				model_info: {
					book_category_id: {
						'label': '類別',
						'type': 'select',
						'choices' : [
							{
								'value': null,
								'display_name': '未分類',
							},
						],
					},
					category_name: {
						'label': '名稱',
						'type': 'text',
					},
				},
			}
		},
		computed: {
			bookinfo_columns: function() {
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
		mounted: function () {
			let self = this

			self.clientg = new $.RestClient('/genericUser/api/');
			self.clientg.add('organizations');
			self.clientg.organizations.read(self.org_id)
			.done(function(data) {
				self.org = data
			})
			.fail(function(xhr, result, statusText){
				alertmessage('error', xhr.responseText)
			})

			self.clientb = new $.RestClient('/ebookSystem/api/');
			self.clientb.add('booksimples');
			self.clientb.add('categorys');
			self.refresh();
		},
		methods: {
			refresh: function(){
				let self = this;
				self.items = []
				self.pointer = {};
				self.model_info = {
					book_category_id: {
						'label': '類別',
						'type': 'select',
						'choices' : [
							{
								'value': null,
								'display_name': '未分類',
							},
						],
					},
					category_name: {
						'label': '名稱',
						'type': 'text',
					},
				}
				self.book_ISBN = '';
				self.book_category_id = 0;
				self.category_id = '';
				self.category_name = '';

				self.clientb.booksimples.read({'org_id': self.org_id, 'category_id': 'null'})
				.done(function(data) {
					let bookinfos = [];
					_.each(data, function(v){
						v.book_info['action'] = v.book_info['ISBN'],
						bookinfos.push(v.book_info);
					})
					self.items.push({
						'id': 0,
						'name': '未分類',
						'book_list': bookinfos,
					})
					self.pointer = self.items[0]
				})
				.fail(function(xhr, result, statusText){
					alertmessage('error', xhr.responseText)
				})

				self.clientb.categorys.read({'org_id': self.org_id})
				.done(function(data) {
					_.each(data, function(v){
						let bookinfos = [];
						_.each(v.book_set, function(v){
							v.book_info['action'] = v.book_info['ISBN'],
							bookinfos.push(v.book_info);
						})
						self.items.push({
							'id': v.id,
							'name': v.name,
							'book_list': bookinfos,
						})

						self.model_info['book_category_id'].choices.push({
							'value': v.id,
							'display_name': v.name,
						})

					})
				})
				.fail(function(xhr, result, statusText){
					alertmessage('error', xhr.responseText)
				})
			},
			book_category_update: function(){
				let self = this

				param = {'category': self.book_category_id}
				self.clientb.booksimples.updatepart(self.book_ISBN, param)
				.done(function(data) {
					alertmessage('success', '書籍類別變更成功');
					self.$refs['bcu' +self.org_id].close();
					self.refresh();
				})
				.fail(function(xhr, result, statusText){
					alertmessage('error', xhr.responseText)
				})
			},
			category_create: function () {
				let self = this;
				self.clientb.categorys.create({
					'org': self.org_id,
					'name': self.category_name,
				})
				.done(function(data) {
					alertmessage('success', '類別新增成功');
					self.$refs['cc' +self.org_id].close();
					self.refresh();
				})
				.fail(function(xhr, result, statusText){
					alertmessage('error', xhr.responseText)
				})
			},
			category_update: function () {
				let self = this;
				self.clientb.categorys.updatepart(self.category_id, {'name': self.category_name})
				.done(function(data) {
					alertmessage('success', '類別名稱變更成功');
					self.$refs['cu' +self.org_id].close();
					self.refresh();
				})
				.fail(function(xhr, result, statusText){
					alertmessage('error', xhr.responseText)
				})
			},
			category_delete: function(item){
				let self = this
				alertconfirm('確認刪除類別:' +item.name)
				.done(function(){
					self.clientb.categorys.del(item.id)
					.done(function(data) {
						alertmessage('success', '成功刪除類別:' +item.name)
						self.refresh()
					})
					.fail(function(xhr, result, statusText){
						alertmessage('error', xhr.responseText)
					})
				})
			},
		},
	}
</script>

<style>
div.panel-heading {
	display: flex;
    justify-content: space-between;
    align-items: center;
}

.list-group-item {
	display: flex;
    justify-content: space-between;
}
</style>