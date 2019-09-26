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
				<a aria-hidden="true" class="navbar-brand" href="/">eDocumentService</a>
				<a class="sr-only" href="/"><h1>eDocumentService</h1></a>
			</div>
			<div id="navbar" class="collapse navbar-collapse navbar-dark bg-inverse">
				<ul class="nav navbar-nav">
					<template v-for="item in item_show(nav_item)">
						<template v-if="item.type=='folder'">
							<li class="dropdown">
								<a class="dropdown-toggle" data-toggle="dropdown" href="#" aria-expanded="false">{{ item.display_name }}<span class="caret"></span></a>
								<ul class="dropdown-menu">
									<template v-for="item in item.items">
										<template v-if="item.type=='item'">
											<li><a :href="item.url">{{ item.display_name }}</a></li>
										</template>
										<template v-if="item.type=='action'">
											<li class="dropdown"><a href="#" @click="item.action()">{{ item.display_name }}</a></li>
										</template>
									</template>
								</ul>
							</li>
						</template>
						<template v-if="item.type=='item'">
							<li class="dropdown"><a :href="item.url">{{ item.display_name }}</a></li>
						</template>
						<template v-if="item.type=='action'">
							<li class="dropdown"><a href="#" @click="item.action()">{{ item.display_name }}</a></li>
						</template>
					</template>
				</ul>
				<ul class="nav navbar-nav navbar-right">
					<template v-for="item in item_show(nav_item_right)">
						<template v-if="item.type=='folder'">
							<li class="dropdown">
								<a class="dropdown-toggle" data-toggle="dropdown" href="#" aria-expanded="false">{{ item.display_name }}<span class="caret"></span></a>
								<ul class="dropdown-menu">
									<template v-for="item in item.items">
										<template v-if="item.type=='item'">
											<li><a :href="item.url">{{ item.display_name }}</a></li>
										</template>
										<template v-if="item.type=='action'">
											<li class="dropdown"><a href="#" @click="item.action()">{{ item.display_name }}</a></li>
										</template>
									</template>
								</ul>
							</li>
						</template>
						<template v-if="item.type=='item'">
							<li class="dropdown"><a :href="item.url">{{ item.display_name }}</a></li>
						</template>
						<template v-if="item.type=='action'">
							<li class="dropdown"><a href="#" @click="item.action()">{{ item.display_name }}</a></li>
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
		data(){
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
								'display_name': '書籍類型管理',
								'permission': ['is_supermanager'],
								'url': '/routing/ebookSystem/category_manager_self/',
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
								'display_name': '書籍閱讀統計',
								'permission': ['is_manager'],
								'url': '/routing/mysite/statistics_book_read/',
							},
							{
								type: 'item',
								'display_name': '志工服務時數統計',
								'permission': ['is_manager'],
								'url': '/routing/mysite/statistics_serviceinfo/',
							},
							{
								type: 'item',
								'display_name': '視障者閱讀統計',
								'permission': ['is_manager'],
								'url': '/routing/mysite/statistics_read/',
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
								'display_name': '統計書籍下載(epub)',
								'permission': ['is_supermanager'],
								'url': '/routing/mysite/statistics/book_download/?file_format=epub',
							},
							{
								type: 'item',
								'display_name': '統計書籍下載(txt)',
								'permission': ['is_supermanager'],
								'url': '/routing/mysite/statistics/book_download/?file_format=txt',
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
						'display_name': '書籍上傳',
						'permission': ['login'],
						'items': [
							{
								type: 'item',
								'display_name': '掃描檔上傳',
								'permission': ['auth_guest', 'is_supermanager', 'is_manager'],
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
						type: 'item',
						'display_name': '校對服務',
						'permission': ['auth_editor'],
						'url': '/routing/ebookSystem/service/',
					},
					{
						type: 'item',
						'display_name': '校對進度',
						'permission': ['auth_guest'],
						'url': '/routing/ebookSystem/book_person/',
					},
					{
						type: 'item',
						'display_name': '我的書櫃',
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
								'url': '/routing/mysite/ddm/',
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
								type: 'action',
								'display_name': '登出',
								'permission': ['true'],
								'action': () => {
									let session_logout = genericUserAPI.userAction.logout()
									let token_logout = token.remove()
									Promise.all([session_logout, token_logout,])
									.then(res => {
										alertmessage('success', '成功登出平台')
										.done(() => {
											window.location.replace('/')
										})
									})
									.catch(res => {
										alertmessage('error', '登錄平台失敗，請確認帳號或密碼是否正確。')
									})
								},
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
								'url': '/routing/about/user_guide/',
							},
							{
								type: 'item',
								'display_name': '平台問與答',
								'permission': ['true'],
								'url': '/routing/genericUser/qanda_all/',
							},
							{
								type: 'item',
								'display_name': '聯絡資訊',
								'permission': ['true'],
								'url': '/routing/about/contact/',
							},
							{
								type: 'item',
								'display_name': '服務條款',
								'permission': ['true'],
								'url': '/routing/about/terms_of_service/',
							},
							{
								type: 'item',
								'display_name': '隱私與資訊安全',
								'permission': ['true'],
								'url': '/routing/about/privacy_and_security/',
							},
							{
								type: 'item',
								'display_name': '平台濫觴',
								'permission': ['true'],
								'url': '/routing/about/origin/',
							},
							{
								type: 'item',
								'display_name': '開發資訊',
								'permission': ['true'],
								'url': '/routing/about/development/',
							},
						],
					},
				],
				user: {},
			}
		},
		created(){
			this.$root.edsnavall = this;
		},
		mounted(){
			this.user = user;
			//this.user = this.$store.state.user;
		},
		methods: {
			item_permission(u, p){
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
			item_show(nav_item) {
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
						if(v.type==='action'){
							item.action = v.action
							items.push(item)
						}
					}
				})
				return items
			},
			mode_change(){
				this.$emit('mode-change')
			},
		},
	}
</script>