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
						@change="refresh()"
					>
						<option :value="0" selected="selected">全部</option>
						<option v-for="item in org_categorys" :value="item.id">{{ item.name }}</option>
					</select>
					<template
						v-if="!choice_org"
					>{{ org.name }}</template>
					<template
						v-for="item in org_categorys"
						v-if="org_id==item.id"
					>
						<select
							class="form-control"
							v-model="category_id"
							id="id_category" name="category"
						>
							<option value="all">全部</option>
							<option
								v-for="category in item.categorys"
								:value="category.id"
							>{{ category.name }}</option>
						</select>
						類別
					</template>
					的文件
				</span>
				<button class="btn btn-lg btn-default" type="button" @click="get_ebook()">領文件</button>
			</form>
			
			<div style="padding:10px; color:#ff2200; font-size:12pt;">注意：未於期限內完成校對動作將自動歸還文件，將無法計入當月服務時數</div>
		</div>

		<div>
			<h3 class="page-header">正校對文件</h3>
			<table-div :datas="edit_ebook" :header="edit_ebook_header">
				<template slot="action" slot-scope="props">
					<a class="btn btn-default" role="button" :href="'/routing/ebookSystem/edit/' +props.item.ISBN_part +'/'">編輯</a>
					<button class="btn btn-default" @click="reback_ebook(props.item.ISBN_part)">還文件</button>
				</template>
			</table-div>
		</div>

		<div>
			<h3 class="page-header">審核中的文件</h3>
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
		data(){
			return {
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
				category_id: 'all',
				org_categorys: [],
			}
		},
		computed: {
			org(){
				let org = {}
				genericUserAPI.organizationRest.read(this.org_id)
				.then(res => {
					org = res.data;
				})
				.catch(res => {
					alertmessage('error', o2j(res.response.data));
				})
				return org
			},
		},
		watch: {
			/*org_id: function() {
				this.refresh()
			},*/
		},
		mounted(){
			this.get_org_category()
			this.refresh()
		},
		methods: {
			get_org_category(){
				genericUserAPI.organizationRest.list()
				.then(res => {
					_.each(res.data, (o) => {
						// org 為 1 屬特殊情形，是一般版使用，故在選擇列表內不顯示
						/*if(o.id==1){
							return -1;
						}*/
						let org_category = {
							'id': o.id,
							'name': o.name,
							'categorys': [],
						}

						ebookSystemAPI.categoryRest.filter({'org_id': o.id})
						.then(res => {
							_.each(res.data, (c) => {
								let temp = {
									'id': c.id,
									'name': c.name,
								}
								org_category.categorys.push(temp)
							})
						})
						.catch(res => {
							alertmessage('error', o2j(res.response.data));
						})
						this.org_categorys.push(org_category)
					})
				})
				.catch(res => {
					alertmessage('error', o2j(res.response.data));
				})

			},
			refresh(){
				if(this.org_id===0){
					query = {'editor_id': user.id, 'status': '2'}
				}
				else {
					query = {'editor_id': user.id, 'status': '2', 'org_id': this.org_id}
				}

				ebookSystemAPI.ebookRest.filter(query)
				.then(res => {
					this.edit_ebook = [];
					_.each(res.data, (v) => {
						this.edit_ebook.push({
							document: v['bookname'] +v['part'],
							page: v.edited_page+1 +'/50',
							get_date: v.get_date,
							deadline: v.deadline,
							status: v.status,
							action: v,
						})
					})
				})

				if(this.org_id===0){
					query = {'editor_id': user.id, 'status': '3'}
				}
				else {
					query = {'editor_id': user.id, 'status': '3', 'org_id': this.org_id}
				}

				ebookSystemAPI.ebookRest.filter(query)
				.then(res => {
					this.finish_ebook = [];
					_.each(res.data, (v) => {
						this.finish_ebook.push({
							document: v['bookname'] +v['part'],
							service_hours: v.service_hours,
							get_date: v.get_date,
							category: v.current_editrecord.category,
							action: v,
						})
					})
				})
			},
			get_ebook(){
				ebookSystemAPI.ebookAction.service({
					'org_id': this.org_id,
					'category_id': this.category_id,
				})
				.then(res => {
					alertmessage('success', '成功取得文件：' +res.data.data.bookname +res.data.data.part)
					.done(() => {
						this.refresh();
					})
				})
				.catch(res => {
					alertmessage('error', o2j(res.response.data));
				})
			},
			reback_ebook(pk){
				alertconfirm('還文件後該文件將提供其他校對者領取，且無法獲得校對時數，是否確定還文件?')
				.done(() => {
					ebookSystemAPI.ebookAction.changeStatus({
						pk: pk,
						direction: '-1',
						status: 'active'
					})
					.then(res => {
						alertmessage('success', '成功歸還文件：' +res.data.data.bookname +res.data.data.part)
						.done(() => {
							this.refresh();
						})
					})
					.catch(res => {
						alertmessage('error', o2j(res.response.data));
					})

				})
			},
			reedit_ebook(pk){
				ebookSystemAPI.ebookAction.changeStatus({
					pk: pk,
					direction: '-1',
					status: 'edit'
				})
				.then(res => {
					alertmessage('success', '成功再編輯文件：' +res.data.data.bookname +res.data.data.part)
					.done(() => {
						this.refresh();
					})
				})
				.catch(res => {
					alertmessage('error', o2j(res.response.data));
				})

			},
		},
	}
</script>