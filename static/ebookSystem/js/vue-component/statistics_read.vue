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
				period: {},
				search_value: '',
				instance_datas: [],
				instance_header: {
					order: '項次',
					username: '姓名',
					join: '訴冊時間',
					online: '閱讀次數',
					checkout: '借閱次數',
					download: '下載次數',
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
				console.log('search')
			},
		},
	}
</script>

<style>

</style>