<template>
	<div>
		<eds_nav_all
			v-if="mode==='all'"
			v-on:mode-change="mode_change('self')"
		></eds_nav_all>
		<eds_nav_self
			v-if="mode==='self'"
			v-on:mode-change="mode_change('all')"
		></eds_nav_self>
	</div>
</template>

<script>
	module.exports = {
		components: {
			'eds_nav_all': components['eds_nav_all'],
			'eds_nav_self': components['eds_nav_self'],
		},
		data(){
			return {
				'mode': 'all', //all, self
			}
		},
		mounted(){
			mode = localStorage.getItem('nav_mode');

			if(!mode) {
				this.mode = 'all'
			}
			else {
				this.mode = mode
			}

		},
		methods: {
			mode_change(mode){
				localStorage.setItem('nav_mode', mode);
				window.location.replace('/')
			},
		},
	}
</script>