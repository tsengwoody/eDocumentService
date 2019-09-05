<template>
	<nav class="navbar navigation-clean-button navbar-fixed-top" role="navigation">
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
								<a class="dropdown-toggle" data-toggle="dropdown" href="#" aria-expanded="false">{|{ item.display_name }|}<span class="caret"></span></a>
								<ul class="dropdown-menu">
									<template v-for="item in item.items">
										<template v-if="item.type=='item'">
											<li><a :href="item.url">{|{ item.display_name }|}</a></li>
										</template>
										<template v-if="item.type=='action'">
											<li class="dropdown"><a href="#" @click="item.action()">{|{ item.display_name }|}</a></li>
										</template>
									</template>
								</ul>
							</li>
						</template>
						<template v-if="item.type=='item'">
							<li class="dropdown"><a :href="item.url">{|{ item.display_name }|}</a></li>
						</template>
						<template v-if="item.type=='action'">
							<li class="dropdown"><a href="#" @click="item.action()">{|{ item.display_name }|}</a></li>
						</template>
					</template>
				</ul>
				<ul class="nav navbar-nav navbar-right">
					<template v-for="item in item_show(nav_item_right)">
						<template v-if="item.type=='folder'">
							<li class="dropdown">
								<a class="dropdown-toggle" data-toggle="dropdown" href="#" aria-expanded="false">{|{ item.display_name }|}<span class="caret"></span></a>
								<ul class="dropdown-menu">
									<template v-for="item in item.items">
										<template v-if="item.type=='item'">
											<li><a :href="item.url">{|{ item.display_name }|}</a></li>
										</template>
										<template v-if="item.type=='action'">
											<li class="dropdown"><a href="#" @click="item.action()">{|{ item.display_name }|}</a></li>
										</template>
									</template>
								</ul>
							</li>
						</template>
						<template v-if="item.type=='item'">
							<li class="dropdown"><a :href="item.url">{|{ item.display_name }|}</a></li>
						</template>
						<template v-if="item.type=='action'">
							<li class="dropdown"><a href="#" @click="item.action()">{|{ item.display_name }|}</a></li>
						</template>
					</template>
					<li class="dropdown"><a href="#" @click="mode_change()">一般版</a></li>
				</ul>
			</div>
		</div>
	</nav>
</template>
<script>
	module.exports = {
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
						'display_name': '書籍上傳',
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
						type: 'item',
						'display_name': '校對服務',
						'permission': ['auth_editor'],
						'url': '/routing/ebookSystem/service_self/',
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
						'url': '/routing/ebookSystem/book_repository_school/',
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
								'display_name': '個人資料',
								'permission': ['true'],
								'url': '/routing/genericUser/user_person/',
							},
							{
								type: 'item',
								'display_name': '服務紀錄',
								'permission': ['auth_editor'],
								'url': '/routing/genericUser/serviceinfo_record/',
							},
							{
								type: 'item',
								'display_name': '校園管理',
								'permission': ['is_manager'],
								'url': '/routing/genericUser/manager_school/',
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
			this.$root.edsnavself = this;
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

<style>
nav.navigation-clean-button {
	background: #badc58;
}

nav.navigation-clean-button a:hover {
	background: #b8e994;
}

.nav .open>a, .nav .open>a:hover, .nav .open>a:focus {
	background-color: #b8e994;
	background: #b8e994;
}

nav.navigation-clean-button li.open a:hover {
	background-color: #b8e994;
}

nav.navigation-clean-button li.open a:active {
	background: #b8e994;
}



nav.navigation-clean-button * {
	color: #333;
}

div.navbar-header {
	font-weight: bold;
    color: inherit;
}


</style>