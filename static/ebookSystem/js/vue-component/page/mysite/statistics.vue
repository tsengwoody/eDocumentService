<template>
	<div>
		<h2>{{ title }}</h2>
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
						<option v-for="(value, key) in orgs" :value="value.id">{{ value.name }}</option>
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
		data(){
			return {
				orgs: [],
				org_id: 'all',
				title: '',
				url: '',
			}
		},
		mounted(){
			genericUserAPI.organizationRest.list()
			.then(res => {
				this.orgs = [],
				_.each(res.data, (v) => {
					this.orgs.push({
						'id': v.id,
						'name': v.name,
					})
				})
			})
			.catch(res => {
				alertmessage('error', o2j(res.response.data));
			})

			let page = window.location.pathname.split('/');
			page = page[page.length-2];
			if(page==='book_download'){
				this.title = '統計書籍下載';
			}
			else if(page==='user_download'){
				this.title = '統計使用者下載';
			}
			else if(page==='user_editrecord'){
				this.title = '統計使用者校對';
			}
			this.url = '/api/statistics/' +page +'/';
			document.title = this.title;
		},
	}
</script>