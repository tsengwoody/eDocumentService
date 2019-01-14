<template>
	<div id="service">
		<div style="text-align: center;">
			<form class="form-inline">
				<span style="margin-right:1em;">
					領取
					<select
						v-if="choice_org"
						class="form-control"
						v-model="org_id"
					>
						<option value="0" selected="selected">全部</option>
						<option v-for="(value, key) in orgs" :value="value.id">{|{ value.name }|}</option>
					</select>
					<template
						v-if="!choice_org"
					>{|{ org.name }|}</template>
					的文件
				</span>
				<button class="btn btn-lg btn-default" type="button" @click="get_ebook()">領文件</button>
			</form>
			
			<div style="padding:10px; color:#ff2200; font-size:12pt;">注意：未於期限內完成校對動作將自動歸還文件，將無法計入當月服務時數</div>
		</div>

		<div>
			<h4 class="page-header">正校對文件</h4>
			<table-div :datas="edit_ebook" :header="edit_ebook_header">
				<template slot="action" slot-scope="props">
					<a class="btn btn-default" role="button" :href="'/routing/ebookSystem/edit/' +props.item.ISBN_part +'/'">編輯</a>
					<button class="btn btn-default" @click="reback_ebook(props.item.ISBN_part)">還文件</button>
				</template>
			</table-div>
		</div>

		<div>
			<h4 class="page-header">審核中的文件</h4>
			<table-div :datas="finish_ebook" :header="finish_ebook_header">
				<template slot="action" slot-scope="props">
					<button class="btn btn-default" @click="reedit_ebook(props.item.ISBN_part)">再編輯</button>
				</template>
			</table-div>
		</div>
	</div>
</template>

<script>
	module.exports = {
		props: ['org_id', 'choice_org',],
		components: {
			'table-div': components['table-div'],
		},
		data: function() {
			return {
				orgs: [],
				edit_ebook_header: {
					document: '文件',
					page: '頁數/總頁數',
					get_date: '領取日期',
					deadline: '期限',
					status: '狀態',
					action: '動作',
				},
				edit_ebook: [],
				finish_ebook_header: {
					document: '文件',
					service_hours: '服務時數',
					get_date: '領取日期',
					category: '類型',
					action: '動作',
				},
				finish_ebook: [],
			}
		},
		computed: {
			org: function () {
				let org = {}
				console.log('YAA')
				this.clientg.organizations.read(this.org_id)
				.done(function(data) {
					org = data
				})
				.fail(function(xhr, result, statusText){
					alertmessage('error', xhr.responseText)
				})
				return org
			},
		},
		created: function () {
			this.clientg = new $.RestClient('/genericUser/api/');
			this.clientg.add('organizations');
			this.clientb = new $.RestClient('/ebookSystem/api/');
			this.clientb.add('ebooks');
			this.clientb.ebooks.addVerb('service', 'POST', {
				'url': 'action/service/',
			})
		},
		mounted: function () {
			document.title = '一般校對';
			let self = this

			this.clientg.organizations.read()
			.done(function(data) {
				_.each(data, function(v){
					self.orgs.push({
						'id': v.id,
						'name': v.name,
					})
				})
			})
			.fail(function(xhr, result, statusText){
				alertmessage('error', xhr.responseText)
			})

			this.refresh()
		},
		methods: {
			refresh: function () {
				// run ajax get data
				let self = this;
				self.clear();

				if(self.org_id===0){
					query = {'editor_id': user.id, 'status': '2'}
				}
				else {
					query = {'editor_id': user.id, 'status': '2', 'org_id': self.org_id}
				}

				self.clientb.ebooks.read(query)
				.done(function(data) {
					_.each(data,function(v){

						self.edit_ebook.push({
							document: v['bookname'] +v['part'],
							page: v.edited_page+1 +'/50',
							get_date: v.get_date,
							deadline: v.deadline,
							status: v.status,
							action: v,
						})
					})
				})

				if(self.org_id===0){
					query = {'editor_id': user.id, 'status': '3'}
				}
				else {
					query = {'editor_id': user.id, 'status': '3', 'org_id': self.org_id}
				}

				self.clientb.ebooks.read(query)
				.done(function(data) {
					_.each(data,function(v){
						self.finish_ebook.push({
							document: v['bookname'] +v['part'],
							service_hours: v.service_hours,
							get_date: v.get_date,
							category: v.current_editrecord.category,
							action: v,
						})
					})
				})
			},
			get_ebook: function () {
				let self = this;

				self.clientb.ebooks.service({'org_id': self.org_id})
				.done(function(data) {
					const ebook = data.data;
					alertmessage('success', '成功取得文件：' +ebook.bookname +ebook.part)
					.done(function () {
						self.refresh();
					})
				})
				.fail(function(xhr, result, statusText){
					data = j2o(xhr.responseText)
					if (data.hasOwnProperty('detail')){
						alertmessage('error', data['detail'])
					}
					else {
						alertmessage('error', xhr.responseText)
					}
				})

			},
			reback_ebook: function (ISBN_part) {
				let self = this;

				alertconfirm('還文件後該文件將提供其他校對者領取，且無法獲得校對時數，是否確定還文件?')
				.done(function(){
					rest_aj_send('post', '/ebookSystem/api/ebooks/' +ISBN_part +'/action/change_status/', {'direction': '-1', 'status': 'active'})
					.done(function(data) {
						const ebook = data['data'].data;
						alertmessage('success', '成功歸還文件：' +ebook.bookname +ebook.part)
						.done(function () {
							self.refresh();
						})
					})
					.fail(function(data){
						alertmessage('error', data['message'])
					})
				})
			},
			reedit_ebook: function (ISBN_part) {
				let self = this;

				rest_aj_send('post', '/ebookSystem/api/ebooks/' +ISBN_part +'/action/change_status/', {'direction': '-1', 'status': 'edit'})
				.done(function(data) {
					const ebook = data['data'].data;
					alertmessage('success', '成功再編輯文件：' +ebook.bookname +ebook.part)
					.done(function () {
						self.refresh();
					})
				})
				.fail(function(data){
					alertmessage('error', data['message'])
				})
			},
			clear: function () {
				this.edit_ebook = [];
				this.finish_ebook = [];
			},
		},
	}
</script>