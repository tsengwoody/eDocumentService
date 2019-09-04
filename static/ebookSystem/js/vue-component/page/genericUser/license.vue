<template>
	<div>
		<h2>平台使用條款</h2>
		<input v-model="agree" type="checkbox" required>
			<span>我同意此條款</span>
		</input>
		<button @click="agree_set()">同意</button>
	</div>
</template>

<script>
	module.exports = {
		data(){
			return {
				agree: true,
			},
		}
		methods: {
			agree_set(){

				if(!this.agree){
					alertmessage('error', '請勾選「我同意此條款」')
				return -1
				}

				genericUserAPI.userRest.partialupdate(user.id, {'is_license': this.agree})
				.then(res => {
					alertmessage('success', '完成簽署條款')
					.done(() => {
						window.location.replace('/')
					})
				})
				.catch(res => {
					alertmessage('error', o2j(res.response.data));
				})
			},
		},
	}
</script>