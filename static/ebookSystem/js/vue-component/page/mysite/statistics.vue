<template>
	<div>
		<h2>{|{ title }|}</h2>
		<div class="form-horizontal" style="margin: 1em 0;">
			<div class="form-group">
				<label class="control-label col-md-2 col-lg-1">
					請選擇單位
				</label>	
				<div class="col-md-4 col-lg-4">
					<select
						class="form-control"
						v-model="org_id"
					>
						<option :value="'all'" selected="selected">全部</option>
						<option v-for="(value, key) in orgs" :value="value.id">{|{ value.name }|}</option>
					</select>
				</div>
			</div>
		</div>
		
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
				org_id: 'all',
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