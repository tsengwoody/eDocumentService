<template>
<div>
	<h3>服務紀錄</h3>

	<tab :headinglevel="4" :data="tab_data">
		<template slot="notyetredeem"  slot-scope="props">
			<h4 style="margin-top:30px;">Step1: 勾選欲兌換之服務紀錄</h4>
			<hr style="margin-top:5px;">
			<div style="margin-bottom:60px;">
				<button class="btn btn-default" @click="editrecord_select_all()">全選</button>
				<button class="btn btn-default" @click="editrecord_checks=[]">全不選</button>
				<button class="btn btn-default" type="Button" @click="editrecord_select_inv()">反向選</button>
				<table-div :datas="editrecords" :header="editrecords_columns">
					<template slot="id" slot-scope="props">
				      	<input type="checkbox" v-model="editrecord_checks" :value="props.item">
				    </template>
				</table-div>
			</div>
			<h4>Step2: 確認後進行兌換</h4>
			<hr style="margin-top:5px;">
			<div style="margin-bottom:60px;">
				<div class="form-inline">
					<div class="form-group" style="margin-right:15px;">
						<label for="sel_exchangecenter" style="margin:0px;">
							選擇兌換中心
							<select v-model="org_select" class="form-control">
								<option
									v-for="item in org_list"
									:value="item.id"
								>
									{|{ item.name }|}
								</option>
							</select>
						</label>
					</div>
				</div>
				<button
					@click="serviceinfo_create()"
					class="btn btn-primary" style="margin-top:10px;"
				>兌換</button>
			</div>
		</template>

		<template slot="redeeming" slot-scope="props">
			<table-div :datas="exchange_false_serviceinfos" :header="exchange_false_serviceinfos_columns">
				<template slot="editrecord_set" slot-scope="props">
					<button class="btn btn-default" @click="editrecords_detail(props.item); openDialog('editrecords_detail', this);">詳細服務紀錄</button>
				</template>
				<template slot="serviceinfo_delete" slot-scope="props">
					<button class="btn btn-default" @click="serviceinfo_delete(props.item);">取消申請</button>
				</template>
			</table-div>

		</template>

		<template slot="redeemed" slot-scope="props">
			<table-div :datas="exchange_true_serviceinfos" :header="exchange_true_serviceinfos_columns">
				<template slot="editrecord_set" slot-scope="props">
					<button class="btn btn-default" @click="editrecords_detail(props.item); openDialog('editrecords_detail', this);">詳細服務紀錄</button>
				</template>
			</table-div>
		</template>
	</tab>

	<div>
		<modal :id_modal="'editrecords_detail'">
			<template slot="header">
				<h4 class="modal-title">詳細服務紀錄</h4>
			</template>

			<template slot="body">
				<table-div :datas="detail_editrecords" :header="detail_editrecords_columns">
			</template>

		</modal>
	</div>

</div>
</template>
<script>
	Vue.options.delimiters = ['{|{', '}|}'];

	module.exports = {
		props: ['user_id',],
		components: {
			'modal': components['modal'],
			'tab': components['tab'],
			'table-div': components['table-div'],
		},
		data: function(){
			return {
				pk: '',
				tab_data: [
					{
						order: 0,
						display_name: '未兌換',
						value: 'notyetredeem',
						type: 'notyetredeem',
						data: '',
					},
					{
						order: 1,
						display_name: '審核中',
						value: 'redeeming',
						type: 'redeeming',
						data: '',
					},
					{
						order: 2,
						display_name: '已兌換',
						value: 'redeemed',
						type: 'redeemed',
						data: '',
					},
				],
				editrecords: [],
				editrecords_columns: {
					id: '核取',
					get_date: '服務時間',
					service_hours: '服務時數',
					stay_hours: '線上時數',
					category: '類型',
				},
				exchange_false_serviceinfos: [],
				exchange_false_serviceinfos_columns: {
					date: '兌換日期',
					service_hours: '服務時數',
					org: '兌換單位',
					editrecord_set: '服務紀錄',
					serviceinfo_delete: '動作',
				},
				exchange_true_serviceinfos: [],
				exchange_true_serviceinfos_columns: {
					date: '兌換日期',
					service_hours: '服務時數',
					org: '兌換單位',
					editrecord_set: '服務紀錄',
				},
				detail_editrecords: [],
				detail_editrecords_columns: {
					part: '文件',
					get_date: '服務時間',
					service_hours: '服務時數',
					stay_hours: '線上時數',
					category: '類型',
				},
				org_list: [],
				editrecord_checks: [],
				org_select: '1',
			}
		},
		computed: {
			transferData: function(){
				return {
					"editrecord_set": this.editrecord_checks,
					"date": moment().format('YYYY-MM-DD'),
					"service_hours": 1000,
					"is_exchange": false,
					"owner": this.pk,
					"org": this.org_select,
				}
			},
			service_hours: function(){
				let self = this

				service_hour = 0
				_.each(self.editrecords, function(v){
					if(_.includes(self.editrecord_checks, v.id)){
						service_hour += v.service_hours
					}
				})
				return service_hour
			},
		},
		watch: {
			user_id: function() {
				this.pk = this.user_id
				this.refresh()
			},
		},
		mounted: function () {
			this.clientg = new $.RestClient('/genericUser/api/');
			this.clientg.add('serviceinfos');
			this.clientg.add('organizations');
			this.clientb = new $.RestClient('/ebookSystem/api/');
			this.clientb.add('editrecords');
			this.pk = this.user_id
		this.refresh()
		},
		methods: {
			instance_set: function (event) {
				this.pk = event
				this.refresh()
			},
			refresh: function(){
				let self = this

				self.editrecords = []
				self.editrecord_checks = []
				self.exchange_false_serviceinfos = []
				self.exchange_true_serviceinfos = []

				query = {'editor_id': self.pk, 'exchange': 'false',}
				self.clientb.editrecords.read(query)
				.done(function(data) {
					_.each(data, function(v){
						temp_data = {
							id: v['id'],
							get_date: v['get_date'],
							service_hours: v['service_hours'],
							stay_hours: v['stay_hours'],
							category: v['category'],
						};
						self.editrecords.push(temp_data);
						self.editrecord_checks.push(v.id)
					})
				})

				query = {'owner_id': self.pk, 'is_exchange': 'false',}
				self.clientg.serviceinfos.read(query)
				.done(function(data) {
					_.each(data, function(v){
						self.exchange_false_serviceinfos.push({
							date: v['date'],
							service_hours: v['service_hours'],
							'org': v['orginfo'].name,
							editrecord_set: v.editrecordinfo_set,
							serviceinfo_delete: v.id,
						})
					})
				})

				query = {'owner_id': self.pk, 'is_exchange': 'true',}
				self.clientg.serviceinfos.read(query)
				.done(function(data) {
					_.each(data, function(v){
						self.exchange_true_serviceinfos.push({
							date: v['date'],
							service_hours: v['service_hours'],
							'org': v['orginfo'].name,
							editrecord_set: v.editrecordinfo_set,
						})
					})
				})

				self.clientg.organizations.read()
				.done(function(data) {
					self.org_list = data
				})
			},
			editrecord_select_all: function(){
				let self = this

				_.each(self.editrecords, function(v){
					self.editrecord_checks.push(v.id)
				})
			},
			editrecord_select_inv: function(){
				let self = this

				temp = []
				_.each(self.editrecords, function(v){
					if(!_.includes(self.editrecord_checks, v.id)){
					temp.push(v.id)
					}
				})
				self.editrecord_checks = temp
			},
			serviceinfo_create: function(){
				let self = this

				if(iser(self.editrecord_checks)){
					alertmessage('error', '請至少選擇一筆服務紀錄。')
					return -1
				}

				if(iser(self.org_select)){
					alertmessage('error', '請選擇兌換中心。')
					return -1
				}

				if(self.service_hours<60){
					alertmessage('error', '單筆申請服務時數需超過1小時。')
					return -1
				}

				self.clientg.serviceinfos.create(self.transferData)
				.done(function(data) {
					alertmessage('success', '申請兌換時數' +o2j(data['service_hours']) +'，請等待核發。')
					self.refresh()

				})
				.fail(function(data){
					alertmessage('error', data['message'])
				})

			},
			serviceinfo_delete: function(id){
				let self = this

				alertconfirm('是否確認取消申請該服務時數(id:' +id +')？')
				.done(function(){
					self.clientg.serviceinfos.del(id)
					.done(function(data) {
						alertmessage('success', '已取消申請兌換時數(id:' +id +')，請重新選擇服務紀錄。')
						self.refresh()
					})
					.fail(function(xhr, result, statusText){
						alertmessage('error', xhr.responseText)
					})
				})

			},
			editrecords_detail: function(editrecords){
				this.detail_editrecords = editrecords
			},
		},
	}

</script>