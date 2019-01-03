<template>
	<div :id="'user_manager' +org_id">
		<h3>{|{ org.name }|}</h3>
		<div>
			<div class="form-inline" style="margin-bottom:20px;">
				<span>關鍵字查詢：</span>
				<select v-model="search_role" class="form-control">
					<option value="all">全部</option>
					<option value="editor">志工</option>
					<option value="guest">視障者</option>
					<option value="unauth">視障者(未驗證)</option>
				</select>
				<input v-model="search_value" class="form-control" type="text" placeholder="輸入欲查詢資訊">
				<button class="btn btn-default" @click="user_refresh('search');">搜尋</button>
			</div>
			<table-div
				:header="user_header"
				:datas="datas"
			>
				<template slot="action" slot-scope="props">
					<button class="btn btn-default" style="margin:0px 3px 3px 0px;" @click="usermodel(props.item.id)">基本資料修改</button>
					<button
						class="btn btn-default"
						@click="
							$refs['up' +org_id].instance_set(props.item.id);
							$refs['um' +org_id].open('user_manager' +org_id);
					">
						權限設定
					</button>
					<button class="btn btn-default"
						v-if="props.item.is_guest"
						@click="
							dm_bus.$emit('instance-set', props.item.disabilitycard_set[0]);
							$refs['dm' +org_id].open('user_manager' +org_id);
					">
						<div v-if="props.item.disabilitycard_set[0]">手冊查閱編修</div>
						<div v-else>手冊新建登錄</div>
					</button>
					<button class="btn btn-default"
						v-if="props.item.is_editor"
						@click="sr_bus.$emit('instance-set', props.item.id); $refs['sr' +org_id].open('user_manager' +org_id)"
					>
						服務紀錄
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

			<modal :id_modal="'sr' +org_id" :ref="'sr' +org_id">
				<template slot="header">
					<h4 class="modal-title">服務紀錄</h4>
				</template>
				<template slot="body">
					<serviceinfo_record
						v-bind:bus="sr_bus"
					>
					</serviceinfo_record>
				</template>
			</modal>

			<modal :id_modal="'um' +org_id" :ref="'um' +org_id">
				<template slot="header">
					<h4 class="modal-title">權限設定</h4>
				</template>
				<template slot="body">
					<user_permission pk="0" :ref="'up' +org_id"></user_permission>
				</template>
				<!--<template slot="footer">
					<button class="btn btn-default" data-dismiss="modal">關閉</button>
					<button class="btn btn-default">儲存</button>
				</template>-->
			</modal>
		</div>
	</div>
</template>
<script>
	module.exports = {
		props: ['org_id',],
		components: {
			'disabilitycard': components['disabilitycard'],
			'modal': components['modal'],
			'serviceinfo_record': components['serviceinfo_record'],
			'table-div': components['table-div'],
			'user_permission': components['user_permission'],
		},
		data: function(){
			return {
				org: {},
				dm_bus: new Vue(),
				sr_bus: new Vue(),
				user_header: {
					"username": "使用者名稱",
					"name": "姓名",
					"email": "電子信箱",
					"phone": "聯絡電話",
					"action": "動作",
				},
				datas: [],
				search_role: 'all', //all/editor/guest
				search_value: '',
				temp_dcpk: '',
			}
		},
		mounted: function () {
			let self = this

			//this.dm_bus.$on('instance-refresh', this.user_refresh)
			this.clientg = new $.RestClient('/genericUser/api/');
			this.clientg.add('users');
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
			user_refresh: function (reason) {
				let self = this;

				if(self.search_role==='unauth'){
					query = {'search': self.search_value, 'auth': 'false'}
				}
				else {
					query = {'search': self.search_value, 'role': self.search_role}
				}
				query['org_id'] = self.org_id

				self.clientg.users.read(query)
				.done(function(data){
					filter_data = []
					_.each(data,function(v){
						temp_data = {
							"username": v.username,
							"name": v.first_name +v.last_name,
							"email": v.email,
							"phone": v.phone,
							"action": v,
						}
						filter_data.push(temp_data)
					})
					self.datas = filter_data
					if(reason==='search'){ alertmessage('success', '查詢完成，共取得 ' +self.datas.length +' 筆資料'); }
				})
				.fail(function(xhr, result, statusText){
					console.log(xhr)
				})


			},
		},
	}
</script>