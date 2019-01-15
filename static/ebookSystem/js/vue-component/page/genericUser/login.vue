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
		data: function(){
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
		mounted: function () {
			document.title = '登入'

			this.client = new $.RestClient('/genericUser/api/')
			this.client.add('users');
			this.client.users.addVerb('login', 'POST', {
				url: 'action/login/',
			});
		},
		methods: {
			login: function () {
				let self = this
				let session_login = rest_aj_send('post', '/genericUser/api/users/action/login/', {
					username: self.username,
					password: self.password,
				})

				let token_login = token.obtain(self.username, self.password)

				token_login
				.done(function(data) {
					token.save();
				})

				Promise.all([session_login, token_login,])
				.then(function (s, t) {
					alertmessage('success', '成功登入平台')
					.done(function() {
						window.location.replace('/')
					})
				})
				.catch(function (s, t) {
					alertmessage('error', '登錄平台失敗，請確認帳號或密碼是否正確。'+o2j(s) +o2j(t))
				})

			},
		},
	}

</script>