<template>
	<div>
		<h2>讀者專區</h2>
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
						'display_name': 'Epub閱讀器下載連結(Windows系統)',
						'permission': ['auth_guest'],
						'url': '',
					},
					{
						type: 'item',
						'display_name': 'Epub閱讀器下載連結(Mac系統)',
						'permission': ['auth_guest'],
						'url': '',
					},
					{
						type: 'item',
						'display_name': 'Epub閱讀器下載連結(Linux系統)',
						'permission': ['auth_guest'],
						'url': '',
					},
					{
						type: 'item',
						'display_name': '平台書庫',
						'permission': ['auth_guest'],
						'url': '/routing/ebookSystem/book_repository_school/',
					},
					{
						type: 'item',
						'display_name': '我的書櫃',
						'permission': ['auth_guest'],
						'url': '/routing/ebookSystem/book_shelf/',
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
			title: '讀者專區',
		},
	}
</script>

<style >
ul.manager_school  {
	line-height: 1.7em;
}
</style>