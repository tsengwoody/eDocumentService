<template>
	<div id="ddm" class="tab-content" style="padding:20px 0px;">
		<h2>法鼓山</h2>
		<div id="ddm">
			<file_manager
				url="/api/ddm/resource/107/"
				:permission="{
					'create': {'is_supermanager': true,},
					'read': {'is_guest': true, 'org2': true,},
					'update': {'is_supermanager': true,},
					'delete': {'is_supermanager': true,},
				}"
			></file_manager>
		</div>
	</div>
</template>

<script>
	module.exports = {
		components: {
			'file_manager': components['file_manager'],
		},
		metaInfo: {
			title: '法鼓山',
		},
	}
</script>