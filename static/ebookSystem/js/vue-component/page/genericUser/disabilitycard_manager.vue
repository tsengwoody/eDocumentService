<template>
	<div>
		<h2>身障手冊管理</h2>
		<tab :data="tab_data">
			<template slot="disabilitycard_manager_org" slot-scope="props">
				<disabilitycard_manager_org :org_id="props.item">
				</disabilitycard_manager_org>
			</template>
		</tab>
	</div>
</template>

<script>
	module.exports = {
		components: {
			'disabilitycard_manager_org': components['disabilitycard_manager_org'],
			'tab': components['tab'],
		},
		data: function() {
			return {
				tab_data: [],
			}
		},
		mounted: function () {
			document.title = '身障手冊管理';
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
						'type': 'disabilitycard_manager_org',
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