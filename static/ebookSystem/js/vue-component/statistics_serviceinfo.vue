<template>
	<div>
		<h3>{{ org.name }}</h3>
		<period v-model="period"></period>
		<formdrf
			:model_info="model['search_value']"
			:field="'search_value'"
			:offset-class="'col-sm-offset-3'"
			v-model="search_value"
		></formdrf>
		<button
			@click="getData"
		>查詢</button>

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
					name: '姓名',
					email: '信箱',
					phone: '電話',
					sh: '時數',
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