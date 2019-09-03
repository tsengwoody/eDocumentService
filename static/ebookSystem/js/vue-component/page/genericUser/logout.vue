<template>
	<div id="logout">
		<div class="container">
			<h2>登出</h2>
			<p>感謝你的服務</p>
		</div>
	</div>
</template>

<script>
	module.exports = {
		metaInfo: {
			title: '登出',
		},
		mounted(){
		},
		methods: {
			logout(){
				let session_logout = genericUserAPI.userAction.logout()
				let token_logout = token.remove()
				Promise.all([session_logout, token_logout,])
				.then(res => {
					alertmessage('success', '成功登出平台')
				})
				.catch(res => {
					alertmessage('error', '登錄平台失敗，請確認帳號或密碼是否正確。')
				})
			},
		},
	}

</script>