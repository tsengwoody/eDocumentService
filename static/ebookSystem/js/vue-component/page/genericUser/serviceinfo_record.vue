<template>
	<div id="serviceinfo" class="container">
		<serviceinfo_record
			:user_id="user.id"
			ref="srcom"
		>
		</serviceinfo_record>
	</div>
</template>
<script>
	module.exports = {
		components: {
			'serviceinfo_record': components['serviceinfo_record'],
		},
		data(){
			return {
				bus: new Vue(),
				pk: '',
			}
		},
		metaInfo: {
			title: '服務紀錄',
		},
		mounted(){
			this.pk = window.location.pathname.split('/')
			this.pk = this.pk[this.pk.length-2]
			if(this.pk==='serviceinfo_record'){
				this.pk = user.id
			}
		},
	}
</script>