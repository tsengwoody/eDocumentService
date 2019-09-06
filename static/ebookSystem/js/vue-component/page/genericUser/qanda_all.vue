<template>
	<div>
		<h2>問與答</h2>
		<tab :headinglevel="3" :data="tab_data">
			<template slot="qanda" slot-scope="props">
				<qanda :category="props.item"></qanda>
			</template>
		</tab>
	</div>
</template>
<script>

	module.exports = {
		components: {
			qanda: components['qanda'],
			'tab': components['tab'],
		},
		data(){
			return {
				tab_data: [
					{
						order: 0,
						display_name: '平台',
						value: 'platform',
						type: 'qanda',
						data: 'platform',
					},
					{
						order: 1,
						display_name: '志工',
						value: 'volunteer',
						type: 'qanda',
						data: 'volunteer',
					},
					{
						order: 2,
						display_name: '視障者',
						value: 'vip',
						type: 'qanda',
						data: 'vip',
					},
				],
			}
		},
		metaInfo: {
			title: '問與答',
		},
	}
</script>