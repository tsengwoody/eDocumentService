<template>
	<div id="retrieve">
		<div class="form-group text-center">
			<h2>取回帳密</h2>
		</div>
		<ul class="nav nav-tabs">
			<li class="active"><a href="#retrieve_reset_password" name="retrieve_tab_grp" data-toggle="tab" aria-expanded="true">重設密碼</a></li>
			<li><a href="#retrieve_get_user" name="retrieve_tab_grp" data-toggle="tab" aria-expanded="false">取回帳號</a></li>
		</ul>
		<div class="tab-content" style="padding:20px 0px;">
			<div id="retrieve_reset_password" class="tab-pane active">
				<h4>重設密碼</h4>
				<div class="form-horizontal">
					<form-drf 
						:model_info="model_info.username"
						:field="'username'"
						v-model="username"
						@keyup.enter.native="reset_password()"
					></form-drf>
					<form-drf 
						:model_info="model_info.birthday_p"
						:field="'birthday_p'"
						v-model="birthday_p"
						@keyup.enter.native="reset_password()"
					></form-drf>
					<div class="form-group">
						<div class="col-sm-3 col-sm-offset-2">
							<button class="form-control btn btn-primary" @click="reset_password()">送出</button>
						</div>
					</div>
				</div>
			</div>
			<div id="retrieve_get_user" class="tab-pane">
				<h4>取回帳號</h4>
				<div class="form-horizontal">
					<form-drf 
						:model_info="model_info.email"
						:field="'email'"
						v-model="email"
						@keyup.enter.native="get_user()"
					></form-drf>
					<form-drf 
						:model_info="model_info.birthday_u"
						:field="'birthday_u'"
						v-model="birthday_u"
						@keyup.enter.native="get_user()"
					></form-drf>
					
					<div class="form-group">
						<div class="col-sm-3 col-sm-offset-2">
							<button class="form-control btn btn-primary" @click="get_user()">送出</button>
						</div>
					</div>
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
				email: '',
				birthday_p: '',
				birthday_u: '',
				model_info: {
					'username': {
						'label': '帳號',
						'type': 'text',
					},
					email: {
						'label': '電子信箱',
						'type': 'text',
					},
					'birthday_p': {
						'label': '生日',
						'type': 'date',
					},
					'birthday_u': {
						'label': '生日',
						'type': 'date',
					},
				},
			}
		},
		computed: {
		},
		mounted: function () {
			document.title = '取回帳密'
		},
		methods: {
			reset_password: function () {
				let self = this
				rest_aj_send('post', '/genericUser/api/users/action/retrieve_up/', {
					action: 'reset_password',
					username: self.username,
					birthday: self.birthday_p,
				})
				.done(function(data) {
					alertmessage('success', '成功重設密碼，請至電子信箱中查閱。')
					.done(function() {
						window.location.replace('/routing/genericUser/login/')
					})
				})
				.fail(function(xhr, result, statusText){
					alertmessage('error', '失敗重設密碼')
				})
			},
			get_user: function () {
				let self = this
				rest_aj_send('post', '/genericUser/api/users/action/retrieve_up/', {
					action: 'get_user',
					email: self.email,
					birthday: self.birthday_u,
				})
				.done(function(data) {
					alertmessage('success', '成功取得帳號，請至電子信箱中查閱。')
				})
				.fail(function(xhr, result, statusText){
					console.log(o2j(xhr))
					alertmessage('error', o2j(xhr))
				})
			},
		},
	}
</script>