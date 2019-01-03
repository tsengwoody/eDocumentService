<template>
	<div>
		<h2>校對文件審核</h2>
		<tab :data="tab_data">
			<template slot="ebook_review_list_org" slot-scope="props">
				<ebook_review_list_org :org_id="props.item">
				</ebook_review_list_org>
			</template>
		</tab>
	</div>
</template>

<script>
	module.exports = {
		components: {
			'ebook_review_list_org': components['ebook_review_list_org'],
			'tab': components['tab'],
		},
		data: function() {
			return {
				tab_data: [],
			}
		},
		mounted: function () {
			document.title = '校對文件審核';
			let self = this

			this.clientg = new $.RestClient('/genericUser/api/');
			this.clientg.add('organizations');
			this.clientg.organizations.read()
			.done(function(data) {
				_.each(data, function(v){
					self.tab_data.push({
						'order': v.id,
						'display_name': v.name,
						'value': v.id,
						'type': 'ebook_review_list_org',
						'data': v.id,
					})
				})
			})
			.fail(function(xhr, result, statusText){
				alertmessage('error', xhr.responseText)
			})
		},
	}
</script>