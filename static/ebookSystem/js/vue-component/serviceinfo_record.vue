<template>
<div>
	<h3>服務紀錄</h3>

	<ul class="nav nav-tabs">
		<li class="active"><a href="#serviceinfo_record_notyetredeem" name="serviceinfo_record_tab_grp" data-toggle="tab" aria-expanded="true">未兌換</a></li>
		<li><a href="#serviceinfo_record_redeeming" name="serviceinfo_record_tab_grp" data-toggle="tab" aria-expanded="false">兌換中</a></li>
		<li><a href="#serviceinfo_record_redeemed" name="serviceinfo_record_tab_grp" data-toggle="tab" aria-expanded="false">已兌換</a></li>
	</ul>
	<div class="tab-content" style="padding:20px 0px;">
		<div id="serviceinfo_record_notyetredeem" class="tab-pane active">
			<h4>未兌換</h4>
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
		</div>

		<div id="serviceinfo_record_redeeming" class="tab-pane">
			<h4>兌換中</h4>
			<table-div :datas="exchange_false_serviceinfos" :header="exchange_serviceinfos_columns">
				<template slot="editrecord_set" slot-scope="props">
					<button class="btn btn-default" @click="editrecords_detail(props.item); openDialog('editrecords_detail', this);">詳細服務紀錄</button>
				</template>
			</table-div>

		</div>

		<div id="serviceinfo_record_redeemed" class="tab-pane">
			<h4>已兌換</h4>
			<table-div :datas="exchange_true_serviceinfos" :header="exchange_serviceinfos_columns">
				<template slot="editrecord_set" slot-scope="props">
					<button class="btn btn-default" @click="editrecords_detail(props.item); openDialog('editrecords_detail', this);">詳細服務紀錄</button>
				</template>
			</table-div>
		</div>

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
</div>
</template>
<script>
	Vue.options.delimiters = ['{|{', '}|}'];

	module.exports = {
		props: ['bus',],
		components: {
			'table-div': httpVueLoader('/static/ebookSystem/js/vue-component/table-div.vue'),
		},
		data: function(){
			return {
				pk: '',
				editrecords: [],
				editrecords_columns: {
					id: '核取',
					get_date: '服務時間',
					service_hours: '服務時數',
					stay_hours: '線上時數',
					category: '類型',
				},
				exchange_false_serviceinfos: [],
				exchange_true_serviceinfos: [],
				exchange_serviceinfos_columns: {
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
					"service_hours": this.service_hours,
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
		created: function () {
			this.clientg = new $.RestClient('/genericUser/api/');
			this.clientg.add('serviceinfos');
			this.clientg.add('organizations');
			this.clientb = new $.RestClient('/ebookSystem/api/');
			this.clientb.add('editrecords');
			this.bus.$on('instance-set', this.instance_set)
		},
		mounted: function () {
			pk = window.location.pathname.split('/')
			pk = pk[pk.length-2]
			if(pk==='serviceinfo_record'){
				this.pk = user.id
			}
			else {
				this.pk = pk
			}
			this.refresh()
		},
		methods: {
			instance_set: function (event) {
				this.pk = event
				console.log('YAA')
				this.refresh()
			},
			refresh: function(){
				let self = this

				self.editrecords = []
				self.editrecord_checks = []
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
			editrecords_detail: function(editrecords){
				this.detail_editrecords = editrecords
			},
		},
	}

</script>