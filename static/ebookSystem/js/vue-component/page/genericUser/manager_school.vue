<template>
	<div>
		<h2>校園管理</h2>
		<ul>
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
						'display_name': '上傳文件審核',
						'permission': ['is_manager'],
						'url': '/routing/ebookSystem/book_review_list_self/',
					},
					{
						type: 'item',
						'display_name': '校對文件審核',
						'permission': ['is_manager'],
						'url': '/routing/ebookSystem/ebook_review_list_self/',
					},
					{
						type: 'item',
						'display_name': '書籍管理',
						'permission': ['is_manager'],
						'url': '/routing/ebookSystem/book_manager_self/',
					},
					{
						type: 'item',
						'display_name': '書籍類型管理',
						'permission': ['is_manager'],
						'url': '/routing/ebookSystem/category_manager_self/',
					},
					{
						type: 'item',
						'display_name': '使用者管理',
						'permission': ['is_manager'],
						'url': '/routing/genericUser/user_manager_self/',
					},
					{
						type: 'item',
						'display_name': '身障手冊管理',
						'permission': ['is_manager'],
						'url': '/routing/genericUser/disabilitycard_manager_self/',
					},
					{
						type: 'item',
						'display_name': '服務時數確認',
						'permission': ['is_manager'],
						'url': '/routing/genericUser/serviceinfo_list_check_self/',
					},
					{
						type: 'item',
						'display_name': '統計書籍下載',
						'permission': ['is_manager'],
						'url': '/routing/mysite/statistics_org/book_download/',
					},
					{
						type: 'item',
						'display_name': '統計書籍下載(epub)',
						'permission': ['is_manager'],
						'url': '/routing/mysite/statistics_org/book_download/?file_format=epub',
					},
					{
						type: 'item',
						'display_name': '統計書籍下載(txt)',
						'permission': ['is_manager'],
						'url': '/routing/mysite/statistics_org/book_download/?file_format=txt',
					},
					{
						type: 'item',
						'display_name': '統計使用者下載',
						'permission': ['is_manager'],
						'url': '/routing/mysite/statistics_org/user_download/',
					},
					{
						type: 'item',
						'display_name': '統計使用者校對',
						'permission': ['is_manager'],
						'url': '/routing/mysite/statistics_org/user_editrecord/',
					},
					{
						type: 'item',
						'display_name': '管理首頁 Banner',
						'permission': ['is_supermanager'],
						'url': '/routing/genericUser/bannercontent_create/',
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
			title: '校園管理',
		},
	}
</script>