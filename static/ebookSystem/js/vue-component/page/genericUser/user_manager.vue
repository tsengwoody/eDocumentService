<template>
	<div>
		<h2>使用者管理</h2>
		<panel_group :data="tab_data" :title="'單位'">
			<template slot="user_manager_org" slot-scope="props">
				<user_manager_org :org_id="props.item">
				</user_manager_org>
			</template>
		</panel_group>
	</div>
</template>

<script>
	module.exports = {
		components: {
			'user_manager_org': components['user_manager_org'],
			'panel_group': components['panel_group'],
		},
		data: function() {
			return {
				tab_data: [],
			}
		},
		mounted: function () {
			document.title = '使用者管理';
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
						'type': 'user_manager_org',
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