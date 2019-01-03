<template>
<div :id="'disabilitycard_manager' +org_id">
	<h3>{|{ org.name }|}</h3>
	<div class="form-inline">
		<div class="form-group">
			<select
				class="form-control"
				v-model="search_filter"
				required
			>
				<option value="all" selected="selected">全部</option>
				<option v-for="(value, key) in search_choices" :value="key">{|{ value }|}</option>
			</select>
		</div>
		<div class="form-group">
			<input v-model="search_value" class="form-control" type="text" placeholder="輸入欲查詢資訊" maxlength="15">
		</div>
		<div class="form-group">
			<button type="button" class="btn btn-primary" @click="search()">搜尋</button>
		</div>
	</div>
	<table-div :datas="search_disabilitycard_datas" :header="disabilitycard_header">
		<template slot="action" slot-scope="props">
			<button class="btn btn-primary"
				@click="
					dm_bus.$emit('instance-set', props.item);
					$refs['dm' +org_id].open('disabilitycard_manager' +org_id);
			">
				查閱編修
			</button>
		</template>
	</table-div>
	<modal :id_modal="'dm' +org_id" :ref="'dm' +org_id">
		<template slot="header">
			<h4 class="modal-title">身心障礙手冊登錄</h4>
		</template>
		<template slot="body">
			<disabilitycard
				:bus="dm_bus"
			>
			</disabilitycard>
		</template>
	</modal>
</div>
</template>
<script>
	module.exports = {
		props: ['org_id',],
		components: {
			'disabilitycard': components['disabilitycard'],
			'modal': components['modal'],
			'table-div': components['table-div'],
		},
		data: function(){
			return {
				org: [],
				dm_bus: new Vue(),
				search_choices: {
					'false': '未啟用',
					'true': '已啟用',
				},
				search_filter: 'all',
				search_value: '',
				disabilitycard_header: {
					"identity_card_number": "身份證字號",
					"name": "姓名",
					"action": "動作",
				},
				search_disabilitycard_datas: [],
			}
		},
		mounted: function () {
			let self = this
			this.clientg = new $.RestClient('/genericUser/api/');
			this.clientg.add('disabilitycards');
			this.clientg.add('organizations');
			this.clientg.organizations.read(this.org_id)
			.done(function(data) {
				self.org = data
			})
			.fail(function(xhr, result, statusText){
				alertmessage('error', xhr.responseText)
			})

		},
		methods: {
			search: function () {
				let self = this;
				self.data = []


				if(self.search_filter==='all'){
					query = {'search': self.search_value, 'org_id': self.org_id}
				}
				else {
					query = {'search': self.search_value, 'is_active': self.search_filter, 'org_id': self.org_id}
				}
				self.clientg.disabilitycards.read(query)
				.done(function(data) {
					let filter_data = []
					_.each(data, function(v){
						temp_data = {
							"identity_card_number": v.identity_card_number,
							"name": v.name,
							"action": v.identity_card_number,
						}

						filter_data.push(temp_data)
					})
					self.search_disabilitycard_datas = filter_data
					alertmessage('success', '查詢完成，共取得 ' +self.search_disabilitycard_datas.length +' 筆資料')
				})
				.fail(function(xhr, result, statusText){
					alertmessage('error', xhr.responseText)
				})

			},
		},
	}
</script>