<template>
	<div>
		<h2>服務時數確認</h2>
		<panel_group :data="tab_data" :title="'單位'">
			<template slot="serviceinfo_list_check_org" slot-scope="props">
				<serviceinfo_list_check_org :org_id="props.item">
				</serviceinfo_list_check_org>
			</template>
		</panel_group>
	</div>
</template>

<script>
	module.exports = {
		components: {
			'serviceinfo_list_check_org': components['serviceinfo_list_check_org'],
			'panel_group': components['panel_group'],
		},
		data: function() {
			return {
				tab_data: [],
			}
		},
		mounted: function () {
			document.title = '服務時數確認';
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
						'type': 'serviceinfo_list_check_org',
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