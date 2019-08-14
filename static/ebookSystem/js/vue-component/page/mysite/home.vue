<template>
	<div>
		<home_all
			v-if="$root.mode==='all'"
		></home_all>
		<home_self
			v-if="$root.mode==='self'"
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
		},
	}
</script>
