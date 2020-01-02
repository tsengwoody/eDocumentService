<template>
	<modal id_modal="spm" ref="spm" :size="'normal'">
		<template slot="header">
			<h4 class="modal-title">修改密碼</h4>
		</template>   
		<template slot="body">
			<div class="form-horizontal">
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
			</div>
		</template>
		<template slot="footer">
			<button class="btn btn-default"
				@click="set_password(user.id)"
			>送出</button>
		</template>
	</modal>
</template>

<script>

	module.exports = {
		components: {
			'modal': components['modal'],
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
				this.$refs['spm'].close()
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