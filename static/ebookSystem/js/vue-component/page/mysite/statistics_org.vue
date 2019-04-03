<template>
	<div>
		<h2>{|{ title }|}</h2>
		<statistics
			:org_id="org_id"
			:url="url"
		>
		</statistics>
	</div>
</template>
<script>
	module.exports = {
		components: {
			'statistics': components['statistics'],
		},
		data: function(){
			return {
				orgs: [],
				org_id: user.org,
				title: '',
				url: '',
			}
		},
		created: function () {
			this.clientg = new $.RestClient('/genericUser/api/');
			this.clientg.add('organizations');
		},
		mounted: function () {
			let self = this

			self.clientg.organizations.read()
			.done(function(data) {
				_.each(data, function(v){
					self.orgs.push({
						'id': v.id,
						'name': v.name,
					})
				})
			})
			.fail(function(xhr, result, statusText){
				alertmessage('error', xhr.responseText)
			})

			let page = window.location.pathname.split('/')
			page = page[page.length-2]
			if(page==='book_download'){
				self.title = '統計書籍下載'
			}
			else if(page==='user_download'){
				self.title = '統計使用者下載'
			}
			else if(page==='user_editrecord'){
				self.title = '統計使用者校對'
			}
			document.title = self.title
			self.url = '/api/statistics/' +page +'/'
		},
		methods: {
		},
	}
</script>