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
		data(){
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
		mounted(){
			genericUserAPI.organizationRest.read(this.org_id)
			.then(res => {
				this.org = res.data;
			})
			.catch(res => {
				alertmessage('error', o2j(res.response.data));
			})
			this.clientb = new $.RestClient('/ebookSystem/api/');
			this.clientb.add('booksimples');
			this.clientb.add('categorys');
			this.refresh();
		},
		methods: {
			refresh(){
				this.items = []
				this.pointer = {};
				this.model_info = {
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
				this.book_ISBN = '';
				this.book_category_id = 0;
				this.category_id = '';
				this.category_name = '';

				ebookSystemAPI.bookSimpleRest.filter({'org_id': this.org_id, 'category_id': 'null'})
				.then(res => {
					let bookinfos = [];
					_.each(res.data, (v) => {
						v.book_info['action'] = v.book_info['ISBN'],
						bookinfos.push(v.book_info);
					})
					this.items.push({
						'id': 0,
						'name': '未分類',
						'book_list': bookinfos,
					})
					this.pointer = this.items[0]
				})
				.catch(res => {
					alertmessage('error', o2j(res.response.data));
				})

				ebookSystemAPI.categoryRest.filter({'org_id': this.org_id})
				.then(res => {
					_.each(res.data, (v) => {
						let bookinfos = [];
						_.each(v.book_set, (v) => {
							v.book_info['action'] = v.book_info['ISBN'],
							bookinfos.push(v.book_info);
						})
						this.items.push({
							'id': v.id,
							'name': v.name,
							'book_list': bookinfos,
						})

						this.model_info['book_category_id'].choices.push({
							'value': v.id,
							'display_name': v.name,
						})

					})
				})
				.catch(res => {
					alertmessage('error', o2j(res.response.data));
				})
			},
			book_category_update(){
				param = {'category': this.book_category_id}
				ebookSystemAPI.bookSimpleRest.partialupdate(this.book_ISBN, param)
				.then(res => {
					alertmessage('success', '書籍類別變更成功');
					this.$refs['bcu' +this.org_id].close();
					this.refresh();
				})
				.catch(res => {
					alertmessage('error', o2j(res.response.data));
				})
			},
			category_create(){
				ebookSystemAPI.categoryRest.create({
					'org': this.org_id,
					'name': this.category_name,
				})
				.then(res => {
					alertmessage('success', '類別新增成功');
					this.$refs['cc' +this.org_id].close();
					this.refresh();
				})
				.catch(res => {
					alertmessage('error', o2j(res.response.data));
				})
			},
			category_update(){
				ebookSystemAPI.categoryRest.partialupdate(this.category_id, {'name': this.category_name})
				.then(res => {
					alertmessage('success', '類別名稱變更成功');
					this.$refs['cu' +this.org_id].close();
					this.refresh();
				})
				.catch(res => {
					alertmessage('error', o2j(res.response.data));
				})
			},
			category_delete(item){
				alertconfirm('確認刪除類別:' +item.name)
				.done(() => {
					ebookSystemAPI.categoryRest.delete(item.id)
					.then(res => {
						alertmessage('success', '成功刪除類別:' +item.name)
						this.refresh()
					})
					.catch(res => {
						alertmessage('error', o2j(res.response.data));
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