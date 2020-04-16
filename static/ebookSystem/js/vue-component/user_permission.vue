<template>
	<div id="permissionDiv" class="row">
		<h4>使用者名稱：{{ username }}</h4>
		<div style="margin:20px;">
			<div v-for="(value, key) in user_permission" style="margin-bottom: 15px;">
				<label><input
					type="checkbox"
					v-model="user_permission[key]"
				>{{ permission_label[key] }}</label>
			</div>
			<button class="btn btn-default" @click="permission_update()">變更</button>
		</div>
	</div>
</template>
<script>
	module.exports = {
		props: ['pk',],
		data(){
			return {
				'username': '',
				user_permission: {
					'is_hot': '',
					'is_active': '',
					'is_manager': '',
					'is_editor': '',
					'is_guest': '',
					'auth_email': '',
					'auth_phone': '',
				},
				permission_label: {
					'is_hot': '關注標記',
					'is_active': '登錄權限',
					'is_manager': '單位管理員權限',
					'is_editor': '志工權限',
					'is_guest': '視障者權限',
					'auth_email': '信箱驗證',
					'auth_phone': '手機驗證',
				},
			}
		},
		mounted(){
			this.refresh()
		},
		methods: {
			instance_set(event){
				this.pk = event
				this.refresh()
			},
			refresh(){
				genericUserAPI.userRest.read(this.pk)
				.then(res => {
					this.username = res.data.username
					_.each(this.user_permission, (v,k) => {
						this.user_permission[k] = res.data[k];
					})
				})
			},
			permission_update(){
				genericUserAPI.userRest.partialupdate(this.pk, this.user_permission)
				.then(res => {
					alertmessage('success', '完成權限變更')
				})
				.catch(res => {
					alertmessage('error', o2j(res.response.data));
				})
			},
		},
	}

</script>
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