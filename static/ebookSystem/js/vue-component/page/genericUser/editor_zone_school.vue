<template>
	<div>
		<h2>志工專區</h2>
		<ul class="manager_school">
			<template v-for="item in itemsShow">
				<li><a :href="item.url" title="(開啟新視窗)" target="blank">{|{ item.display_name }|}</a></li>
			</template>
		</ul>
	</div>
</template>
<script>
	module.exports = {
		components: {
		},
		data(){
			return {
				items: 				[
					{
						type: 'item',
						'display_name': '服務紀錄',
						'permission': ['auth_editor'],
						'url': '/routing/genericUser/serviceinfo_record/',
					},
					{
						type: 'item',
						'display_name': '個人資料',
						'permission': ['true'],
						'url': '/routing/genericUser/user_person/',
					},
				],
			}
		},
		computed: {
			itemsShow(){
				//let user = this.user;
				let temp = [];
				this.items.forEach(v => {
					if(v.permission.includes('true')){ 
						temp.push(v);
					}
					if(v.permission.includes('anonymous') && iser(user)){
						temp.push(v);
					}
					if(v.permission.includes('login') && !iser(user)){
						temp.push(v);
					}
					if(!iser(user)){
						let add = false;
						let roles = ['is_editor', 'is_guest', 'auth_editor', 'auth_guest', 'is_manager', 'is_supermanager', 'is_superuser']
						roles.forEach(role => {
							if(v.permission.includes(role) && user[role] && (!add)){
								temp.push(v);
								add = true;

							}
						})
					}
				})
				return temp;
			},
		},
		metaInfo: {
			title: '志工專區',
		},
	}
</script>

<style >
ul.manager_school  {
	line-height: 1.7em;
}
</style>