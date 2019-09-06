<template>
	<div :id="'serviceinfo_check' +org_id">
		<h3>{{ org.name }}</h3>
		<h3 style="margin-top:30px;">Step1: 勾選志工所提送的兌換項目</h3>
		<hr style="margin-top:5px;">
		<div style="margin-bottom:60px;">
			<button class="btn btn-default" @click="serviceinfo_select_all()">全選</button>
			<button class="btn btn-default" @click="serviceinfo_checks=[]">全不選</button>
			<button class="btn btn-default" @click="serviceinfo_select_inv()">反向選</button>
			<button class="btn btn-default" onclick="window.location.replace('/genericUser/api/serviceinfos/action/exchange_false_export/')">匯出</button>
			<table-div :datas="serviceinfo_datas" :header="serviceinfo_header">
				<template slot="check" slot-scope="props">
					<input type="checkbox" v-model="serviceinfo_checks" :value="props.item.id">
				</template>
				<template slot="editrecord_set" slot-scope="props">
					<button
						class="btn btn-default"
						@click="
							editrecords_detail(props.item);
							openDialog('editrecords_detail' +org_id, this);
						">詳細服務紀錄</button>
				</template>
			</table-div>
		</div>
		<h3>Step2: 確認後進行兌換</h3>
		<hr style="margin-top:5px;">
		<div style="margin-bottom:60px;">
			<button
				@click="serviceinfo_cancel()"
				class="btn btn-primary" style="margin-top:10px;"
			>退回兌換</button>
			<button
				@click="serviceinfo_exchange()"
				class="btn btn-primary" style="margin-top:10px;"
			>同意兌換</button>
		</div>
		<modal :id_modal="'editrecords_detail' +org_id">
			<template slot="header">
				<h4 class="modal-title">詳細服務紀錄</h4>
			</template>
			<template slot="body">
				<table-div :datas="detail_editrecord_datas" :header="detail_editrecord_header">
			</template>
		</modal>
	</div>
</template>
<script>
	module.exports = {
		props: ['org_id',],
		components: {
			'modal': components['modal'],
			'table-div': components['table-div'],
		},
		data(){
			return {
				org: [],
				serviceinfo_header: {
					'check': '核取',
					'date': '兌換日期',
					'service_hours': '服務時數',
					'user': '服務者',
					'org': '兌換單位',
					editrecord_set: '服務紀錄',
				},
				serviceinfo_datas: [],
				serviceinfo_checks: [],
					detail_editrecord_datas: [],
					detail_editrecord_header: {
						part: '文件',
						get_date: '服務時間',
						service_hours: '服務時數',
						stay_hours: '線上時數',
						category: '類型',
					},
				detail_editrecord_datas: [],
			}
		},
		mounted(){
			genericUserAPI.organizationRest.read(this.org_id)
			.then(res => {
				this.org = res.data
			})
			.catch(res => {
				alertmessage('error', o2j(res.response.data));
			})
			this.get_serviceinfo_data();
		},
		methods: {
			get_serviceinfo_data(){
				this.serviceinfo_datas = [];
				genericUserAPI.serviceInfoRest.filter({'is_exchange': 'false', 'org_id': this.org_id})
				.then(res => {
					_.each(res.data, (v) => {
						this.serviceinfo_datas.push({
							'check': v,
							'date': v.date,
							'service_hours': v.service_hours,
							'user': v.userinfo.username,
							'org': v.orginfo.name,
							editrecord_set: v.editrecordinfo_set,
						})
					})
				})
				.catch(res => {
					alertmessage('error', o2j(res.response.data));
				})
			},
			serviceinfo_exchange(){
				if(iser(this.serviceinfo_checks)){
					alertmessage('error', '請至少選擇一筆兌換紀錄。')
					return -1
				}

				let dfs = [];
				_.each(this.serviceinfo_checks, (v) => {
					dfs.push(genericUserAPI.serviceInfoRest.partialupdate(v, { 'is_exchange': true }));
				})

				Promise.all(dfs)
				.then(res => {
					alertmessage('success', '同意兌換成功')
					.done(() => {
						this.get_serviceinfo_data();
					})
				})
				.catch(res => {
					alertmessage('error', o2j(res.response.data));
				})
			},
			serviceinfo_cancel(){
				if(iser(this.serviceinfo_checks)){
					alertmessage('error', '請至少選擇一筆兌換紀錄。')
					return -1
				}

				let dfs = [];
				_.each(this.serviceinfo_checks, (v) => {
					dfs.push(genericUserAPI.serviceInfoRest.delete(v));
				})

				Promise.all(dfs)
				.then(res => {
					alertmessage('success', '退回兌換申請')
					.done(() => {
						this.get_serviceinfo_data();
					})
				})
				.catch(res => {
					alertmessage('error', o2j(res.response.data));
				})
			},
			serviceinfo_select_all(){
				_.each(this.serviceinfo_datas, (v) => {
					this.serviceinfo_checks.push(v.check.id);
				})
			},
			serviceinfo_select_inv(){
				let temp = [];
				_.each(this.serviceinfo_datas, (v) => {
					if(!_.includes(this.serviceinfo_checks, v.check.id)){
					temp.push(v.check.id);
					}
				})
				this.serviceinfo_checks = temp
			},
			editrecords_detail(editrecords){
				this.detail_editrecord_datas = editrecords;
			},
		},
	}
</script>