<style scoped>

#permissionDiv {
	padding: 0px 0px 0px 20px; 
	background-color:#fafafa;
}

input[type=checkbox] {
	margin:0px 3px 0px 0px; 
	padding:0px; 
	cursor:pointer;
}

</style>

<template id="user_permission">
	<div id="permissionDiv" class="row">
		<h4>使用者名稱：{|{ username }|}</h4>
		<div style="margin:20px;">
			<div v-for="(value, key) in user_permission" style="margin-bottom: 15px;">
				<label><input
					type="checkbox"
					v-model="user_permission[key]"
				>{|{ permission_label[key] }|}</label>
			</div>
			<button class="btn btn-default" @click="permission_update()">變更</button>
		</div>
	</div>
</template>
<script>

	Vue.options.delimiters = ['{|{', '}|}'];

	Vue.component('user_permission', {
		template: '#user_permission',
		props: ['pk',],
		data: function(){
			return {
				'username': '',
				user_permission: {
					'is_active': '',
					'is_editor': '',
					'is_guest': '',
					'auth_email': '',
					'auth_phone': '',
				},
				permission_label: {
					'is_active': '登錄權限',
					'is_editor': '志工權限',
					'is_guest': '視障者權限',
					'auth_email': '信箱驗證',
					'auth_phone': '手機驗證',
				},
			}
		},
		created: function () {
			let self = this
			self.client = new $.RestClient('/genericUser/api/')
			self.client.add('users');
		},
		mounted: function () {
			this.refresh()
		},
		methods: {
			instance_set: function (event) {
				this.pk = event
				this.refresh()
			},
			refresh: function () {
				let self = this
				self.client.users.read(self.pk)
				.done(function(data) {
					self.username = data.username
					_.each(self.user_permission, function(v,k){
						self.user_permission[k] = data[k]
					})
				})
			},
			permission_update: function () {
				let self = this
				self.client.users.updatepart(self.pk, self.user_permission)
				.done(function(data) {
					alertmessage('success', '完成權限變更')
				})
				.fail(function(xhr, result, statusText){
					alertmessage('error', xhr.responseText)
				})
			},
		},
	})

</script>