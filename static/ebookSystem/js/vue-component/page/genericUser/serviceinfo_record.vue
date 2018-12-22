<template>
	<div id="serviceinfo" class="container">
		<serviceinfo_record
			:bus="bus"
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
		data: function(){
			return {
				bus: new Vue(),
				pk: '',
			}
		},
		mounted: function () {
			document.title = '服務紀錄'
			this.pk = window.location.pathname.split('/')
			this.pk = this.pk[this.pk.length-2]
			if(this.pk==='serviceinfo_record'){
				this.pk = user.id
			}
			setTimeout(() => {
				//this.bus.$emit('instance-set', this.pk)
				//this.$refs.srcom.pk=this.pk
				//this.$refs.srcom.refresh()
			}, 1000)
		},
	}
</script>