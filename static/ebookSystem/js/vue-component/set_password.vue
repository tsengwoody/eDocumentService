<template>
	<div>
			<form-drf 
				:model_info="model_info.old_password"
				:input-class="'col-sm-5'"
				:field="'old_password'"
				:offset-class="'col-sm-offset-3'"
				v-model="old_password"
				@keyup.enter.native="set_password(user.id)"
			></form-drf>

			<form-drf 
				:model_info="model_info.new_password1"
				:input-class="'col-sm-5'"
				:field="'new_password1'"
				:offset-class="'col-sm-offset-3'"
				v-model="new_password1"
				@keyup.enter.native="set_password(user.id)"
			></form-drf>

			<form-drf 
				:model_info="model_info.new_password2"
				:input-class="'col-sm-5'"
				:field="'new_password2'"
				:offset-class="'col-sm-offset-3'"
				v-model="new_password2"
				@keyup.enter.native="set_password(user.id)"
			></form-drf>
	</div>
</template>

<script>

	module.exports = {
		components: {
			'form-drf': components['form'],
		},
		data(){
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
		methods: {
			set_password(pk){
				genericUserAPI.userAction.setPassword(pk, {
					old_password: this.old_password,
					new_password1: this.new_password1,
					new_password2: this.new_password2,
				})
				.then(res => {
					this.$root.$message.open({message: '成功修改密碼'})
					//alertmessage('success', '成功修改密碼')
				})
				.catch(res => {
					this.$root.$message.open({message: o2j(res.response.data)})
					//alertmessage('error', o2j(res.response.data));
				})
			},
		},
	};

</script>