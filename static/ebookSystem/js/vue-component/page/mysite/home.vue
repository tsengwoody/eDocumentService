<template>
	<div>
		<home_all
			v-if="mode==='all'"
		></home_all>
		<home_self
			v-if="mode==='self'"
		></home_self>
	</div>
</template>

<script>
	module.exports = {
		components: {
			'home_all': components['home_all'],
			'home_self': components['home_self'],
		},
		data(){
			return {
			}
		},
		metaInfo: {
			title: '首頁',
		},
		mounted(){
			mode = localStorage.getItem('nav_mode');
			if (!(mode=='all') && !(mode=='self')) {
				this.mode = 'all';
			}
		},
		computed: {
		},
		methods: {
		},
	}
</script>
