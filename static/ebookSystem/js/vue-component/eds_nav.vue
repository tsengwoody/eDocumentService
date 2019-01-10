<template>
	<nav class="navbar navbar-inverse navbar-fixed-top" role="navigation">
		<div class="container">
			<div class="navbar-header">
				<button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar">
					<span class="sr-only">功能選單</span>
					<span class="icon-bar"></span>
					<span class="icon-bar"></span>
					<span class="icon-bar"></span>
				</button>
				<a class="navbar-brand" href="/">eDocumentService</a>
			</div>
			<div id="navbar" class="collapse navbar-collapse navbar-dark bg-inverse">
				<ul class="nav navbar-nav">
					<template v-for="item in item_show(nav_item)">
						<template v-if="item.type=='folder'">
							<li class="dropdown">
								<a class="dropdown-toggle" data-toggle="dropdown" href="#" aria-expanded="false">{|{ item.display_name }|}<span class="caret"></span></a>
								<ul class="dropdown-menu">
									<template v-for="folder_item in item.items">
									<li><a :href="folder_item.url">{|{ folder_item.display_name }|}</a></li>
									</template>
								</ul>
							</li>
						</template>
						<template v-if="item.type=='item'">
							<li class="dropdown"><a :href="item.url">{|{ item.display_name }|}</a></li>
						</template>
					</template>
				</ul>
				<ul class="nav navbar-nav navbar-right">
					<template v-for="item in item_show(nav_item_right)">
						<template v-if="item.type=='folder'">
							<li class="dropdown">
								<a class="dropdown-toggle" data-toggle="dropdown" href="#" aria-expanded="false">{|{ item.display_name }|}<span class="caret"></span></a>
								<ul class="dropdown-menu">
									<template v-for="folder_item in item.items">
									<li><a :href="folder_item.url">{|{ folder_item.display_name }|}</a></li>
									</template>
								</ul>
							</li>
						</template>
						<template v-if="item.type=='item'">
							<li class="dropdown"><a :href="item.url">{|{ item.display_name }|}</a></li>
						</template>
					</template>
					<li class="dropdown"><a href="#" @click="mode_change()">校園版</a></li>
				</ul>
			</div>
		</div>
	</nav>
</template>
<script>
	module.exports = {
		components: {
		},
		data: function(){
			return {
				'nav_item': [
					{
						type: 'item',
						'display_name': '網站導覽',
						'permission': ['true'],
						'url': '/routing/mysite/sitemap/',
					},
					{
						type: 'folder',
						'display_name': '管理',
						'permission': ['login'],
						'items': [
							{
								type: 'item',
								'display_name': '上傳文件審核',
								'permission': ['is_supermanager'],
								'url': '/routing/ebookSystem/book_review_list/',
							},
							{
								type: 'item',
								'display_name': '校對文件審核',
								'permission': ['is_supermanager'],
								'url': '/routing/ebookSystem/ebook_review_list/',
							},
							{
								type: 'item',
								'display_name': '書籍管理',
								'permission': ['is_supermanager'],
								'url': '/routing/ebookSystem/book_manager/',
							},
							{
								type: 'item',
								'display_name': '使用者管理',
								'permission': ['is_supermanager'],
								'url': '/routing/genericUser/user_manager/',
							},
							{
								type: 'item',
								'display_name': '身障手冊管理',
								'permission': ['is_supermanager'],
								'url': '/routing/genericUser/disabilitycard_manager/',
							},
							{
								type: 'item',
								'display_name': '服務時數確認',
								'permission': ['is_supermanager'],
								'url': '/routing/genericUser/serviceinfo_list_check/',
							},
							{
								type: 'item',
								'display_name': '校對順序',
								'permission': ['is_supermanager'],
								'url': '/routing/ebookSystem/bookorder_list/',
							},
							{
								type: 'item',
								'display_name': '統計資訊',
								'permission': ['is_supermanager'],
								'url': '/statistics_old/',
							},
							{
								type: 'item',
								'display_name': '統計書籍下載',
								'permission': ['is_supermanager'],
								'url': '/routing/mysite/statistics/book_download/',
							},
							{
								type: 'item',
								'display_name': '統計使用者下載',
								'permission': ['is_supermanager'],
								'url': '/routing/mysite/statistics/user_download/',
							},
							{
								type: 'item',
								'display_name': '統計使用者校對',
								'permission': ['is_supermanager'],
								'url': '/routing/mysite/statistics/user_editrecord/',
							},
							{
								type: 'item',
								'display_name': '管理首頁 Banner',
								'permission': ['is_supermanager'],
								'url': '/routing/genericUser/bannercontent_create/',
							},
							{
								type: 'item',
								'display_name': '訊息傳送',
								'permission': ['is_supermanager'],
								'url': '/routing/genericUser/user_email/',
							},
							{
								type: 'item',
								'display_name': '公告發佈',
								'permission': ['is_supermanager'],
								'url': '/routing/genericUser/announcement_create/',
							},
							{
								type: 'item',
								'display_name': '分段管理',
								'permission': ['is_superuser'],
								'url': '/routing/ebookSystem/ebook_manager/',
							},
						],
					},
					{
						type: 'folder',
						'display_name': '單位管理',
						'permission': ['login'],
						'items': [
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
						],
					},
					{
						type: 'folder',
						'display_name': '文件上傳',
						'permission': ['login'],
						'items': [
							{
								type: 'item',
								'display_name': '掃描檔上傳',
								'permission': ['auth_guest'],
								'url': '/routing/ebookSystem/book_create/',
							},
							{
								type: 'item',
								'display_name': '電子檔上傳',
								'permission': ['is_supermanager'],
								'url': '/routing/ebookSystem/book_upload/',
							},
						],
					},
					{
						type: 'folder',
						'display_name': '校對服務',
						'permission': ['login'],
						'items': [
							{
								type: 'item',
								'display_name': '一般校對',
								'permission': ['auth_editor'],
								'url': '/routing/ebookSystem/service/',
							},
						],
					},
					{
						type: 'item',
						'display_name': '校對進度',
						'permission': ['auth_guest'],
						'url': '/routing/ebookSystem/book_person/',
					},
					{
						type: 'item',
						'display_name': '借閱書櫃',
						'permission': ['auth_guest'],
						'url': '/routing/ebookSystem/book_shelf/',
					},
					{
						type: 'item',
						'display_name': '平台書庫',
						'permission': ['true'],
						'url': '/routing/ebookSystem/book_repository/',
					},
					{
						type: 'folder',
						'display_name': '專案合作',
						'permission': ['true'],
						'items': [
							{
								type: 'item',
								'display_name': '法鼓山(107年度)',
								'permission': ['true'],
								'url': '/generics/ddm/',
							},
						],
					},
				],
				'nav_item_right': [
					{
						type: 'folder',
						'display_name': '帳號',
						'permission': ['login'],
						'items': [
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
							{
								type: 'item',
								'display_name': '登出',
								'permission': ['true'],
								'url': '/auth/logout/',
							},
						],
					},
					{
						type: 'item',
						'display_name': '登入',
						'permission': 'anonymous',
						'url': '/routing/genericUser/login/',
					},
					{
						type: 'item',
						'display_name': '註冊',
						'permission': 'anonymous',
						'url': '/routing/genericUser/register/',
					},
					{
						type: 'folder',
						'display_name': '關於',
						'permission': ['true'],
						'items': [
							{
								type: 'item',
								'display_name': '教學內容',
								'permission': ['true'],
								'url': '/routing/genericUser/qanda_tutorial/',
							},
							{
								type: 'item',
								'display_name': '平台使用指南',
								'permission': ['true'],
								'url': '/about/user_guide/',
							},
							{
								type: 'item',
								'display_name': '平台Q&A',
								'permission': ['true'],
								'url': '/about/qanda/',
							},
							{
								type: 'item',
								'display_name': '聯絡資訊',
								'permission': ['true'],
								'url': '/about/contact/',
							},
							{
								type: 'item',
								'display_name': '服務條款',
								'permission': ['true'],
								'url': '/about/terms_of_service/',
							},
							{
								type: 'item',
								'display_name': '隱私與資訊安全',
								'permission': ['true'],
								'url': '/about/privacy_and_security/',
							},
							{
								type: 'item',
								'display_name': '平台濫觴',
								'permission': ['true'],
								'url': '/about/origin/',
							},
							{
								type: 'item',
								'display_name': '開發資訊',
								'permission': ['true'],
								'url': '/about/development/',
							},
							{
								type: 'item',
								'display_name': '營運組織',
								'permission': ['true'],
								'url': 'https://www.forblind.org.tw/',
							},
						],
					},
				],
				user: {},
			}
		},
		computed: {
		},
		created: function () {
		},
		mounted: function () {
			this.user = user
		},
		methods: {
			item_permission: function(u, p){
				if(p.includes('true')){ return true }
				if(p.includes('false')){ return false }
				if(p.includes('anonymous')){
					if(iser(u)){ return true}
					else { return false}
				}
				if(!iser(u)){
					if(p.includes('login')){
						return true
					}
					roles = ['is_editor', 'is_guest', 'auth_editor', 'auth_guest', 'is_manager', 'is_supermanager', 'is_superuser']
					for(var i=0; i<roles.length; i++){
						role = roles[i]
						if(p.includes(role)){
							return u[role]
						}
					}
				}
				else {
					return false
				}
			},
			'item_show': function item_show(nav_item) {
				let items = []
				_.each(nav_item, v => {
					if(this.item_permission(this.user, v.permission)){
						let item = {
							'type': v.type,
							'display_name': v.display_name,
						}
						if(v.type==='folder'){
							item.items = this.item_show(v.items)
							if(item.items.length>0){
								items.push(item)
							}
						}
						if(v.type==='item'){
							item.url = v.url
							items.push(item)
						}
					}
				})
				return items
			},
			mode_change: function(){
				let self = this
				self.$emit('mode-change')
			},
		},
	}
</script>