<template>
	<div>
			<form-drf 
				:model_info="model_info.old_password"
				:input-class="'col-sm-5'"
				:field="'old_password'"
				:offset-class="'col-sm-offset-3'"
				v-model="old_password"
				@keyup.enter.native="set_password()"
			></form-drf>

			<form-drf 
				:model_info="model_info.new_password1"
				:input-class="'col-sm-5'"
				:field="'new_password1'"
				:offset-class="'col-sm-offset-3'"
				v-model="new_password1"
				@keyup.enter.native="set_password()"
			></form-drf>

			<form-drf 
				:model_info="model_info.new_password2"
				:input-class="'col-sm-5'"
				:field="'new_password2'"
				:offset-class="'col-sm-offset-3'"
				v-model="new_password2"
				@keyup.enter.native="set_password()"
			></form-drf>
	</div>
</template>

<script>

	module.exports = {
		components: {
			'form-drf': httpVueLoader('/static/ebookSystem/js/vue-component/form.vue'),
		},
		data: function(){
			return {
				old_password: '',
				new_password1: '',
				new_password2: '',
				model_info: {
					'old_password': {
						'label': '舊密碼',
						'type': 'password',
					},
					'new_password1': {
						'label': '新密碼',
						'type': 'password',
					},
					'new_password2': {
						'label': '確認新密碼',
						'type': 'password',
					},
				},
			}
		},
		computed: {
		},
		mounted: function(){
		},
		methods: {
			set_password: function(){
				let self = this
				rest_aj_send('post', '/genericUser/api/users/' +user.id +'/action/set_password/', {
					old_password: self.old_password,
					new_password1: self.new_password1,
					new_password2: self.new_password2,
				})
				.done(function(data) {
					alertmessage('success', '成功修改密碼')
				})
				.fail(function(xhr, result, statusText){
					alertmessage('error', '失敗修改密碼')
				})
			},
		},
	};

</script>