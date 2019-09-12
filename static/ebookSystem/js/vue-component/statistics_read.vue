<template>
	<div>
		<h3>{{ org.name }}</h3>
		<div class="form-horizontal" style="margin-top: 1em;">
			<period v-model="period"></period>
			<formdrf
				:model_info="model['search_value']"
				:field="'search_value'"
				:label-class="'col-sm-2'"
				v-model="search_value"
			></formdrf>
			<div class="form-group">
				<label class="control-label col-sm-2 offset-sm-1"></label>
				<div class="col-sm-3">	
					<button
						class="btn btn-default"
						@click="getData"
					>查詢</button>
				</div>
			</div>
		</div>

		<table-div
			:header="instance_header"
			:datas="instance_datas"
		>
		</table-div>
	</div>
</template>

<script>
	module.exports = {
		props: {
			org: Object,
		},
		components: {
			formdrf: components['form'],
			period: components['period'],
			tableDiv: components['table-div'],
		},
		data(){
			return {
				url: '/api/statistics/user_read/',
				period: {},
				search_value: '',
				instance_datas: [],
				instance_header: {
					order: '項次',
					name: '姓名',
					join: '註冊日',
					library: '借閱',
					download: '下載',
				},
				model: {
					search_value: {
						'label': '查詢字',
						'type': 'text',
					required: true,
					},
				},
			}
		},
		methods: {
			getData(){
				let rdate = /^\d{4,4}-\d{2,2}-\d{2,2}$/;
				if (!rdate.test(this.period.begin)){
					alertmessage('error', '開始日期格式錯誤');
					return -1;
				}
				if (!rdate.test(this.period.end)){
					alertmessage('error', '結束日期格式錯誤');
					return -1;
				}

				let params = {org_id: this.org.id, ...{
					begin_time: this.period['begin'],
					end_time: this.period['end'],
				}}
				this.instance_datas = [];
				axios.get(this.url, {params: params})
				.then(res => {
					res.data.forEach((v, i) => {
						this.instance_datas.push({
							order: i,
							name: v.user,
							join: v.join,
							library: v.library,
							download: v.download,
						})
					})
					alertmessage('success', '查詢完成，共取得 ' +this.instance_datas.length +' 筆資料')
				})
				.catch(res => {
					alertmessage('error', o2j(res.response.data));
				})

			},
		},
	}
</script>

<style>

</style>