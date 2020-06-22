<template>
<div id="login">
	<div class="form-group text-center">
		<h2>登錄</h2>
	</div>
	<div class="form-horizontal">
		<form-drf 
			:model_info="model_info.username"
			:field="'username'"
			:offset-class="'col-sm-offset-3'"
			v-model="username"
			@keyup.enter.native="login()"
		></form-drf>

		<form-drf 
			:model_info="model_info.password"
			:field="'password'"
			:offset-class="'col-sm-offset-3'"
			v-model="password"
			@keyup.enter.native="login()"
		></form-drf>

		<div class="form-group">
			<div class="col-sm-3 col-sm-offset-5">
				<button class="form-control btn btn-primary" @click="login()">登錄</button>
			</div>
		</div>
		<div class="form-group">
			<div class="col-sm-3 col-sm-offset-5">
				<a href="/routing/genericUser/retrieve/">忘記帳密</a>
			</div>
		</div>
	</div>
</div>
</template>

<script>
	module.exports = {
		components: {
			'form-drf': components['form'],
		},
		data(){
			return {
				username: '',
				password: '',
				model_info: {
					'username': {
						'label': '帳號',
						'type': 'text',
					},
					password: {
						'label': '密碼',
						'type': 'password',
					},
				},
			}
		},
		metaInfo: {
			title: '登入',
		},
		mounted(){
		},
		methods: {
			login(){
				let session_login = genericUserAPI.userAction.login(this.username, this.password)
				//let token_login = token.obtain(this.username, this.password)
				Promise.all([session_login,])
				.then(res => {
					alertmessage('success', '成功登入平台')
					.done(() => {
						window.location.replace('/')
					})
				})
				.catch(res => {
					this.username = '';
					this.password = '';
					alertmessage('error', '登錄平台失敗，請確認帳號或密碼是否正確。')
				})

			},
		},
	}

</script>