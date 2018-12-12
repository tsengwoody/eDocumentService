<template>
<div>
	<table-div :datas="datas" :header="header">
		<template slot="action" slot-scope="props">
			<button class="btn btn-default" @click="check_create(props.item)">借閱</button>
			<a class="btn btn-default" role="button"
				:href="'/ebookSystem/library_origin_view?ISBN=' +props.item"
				target="_blank" title="閱讀(另開新視窗)"
			>閱讀</a>
		</template>
	</table-div>
</div>
</template>

<script>

	module.exports = {
		props: ['header', 'datas',],
		components: {
			'table-div': components['table-div'],
		},
		data: function(){
			return {
			}
		},
		methods: {
			check_create: function (pk) {
				let self = this

				rest_aj_send('post', '/ebookSystem/api/libraryrecords/action/check_create/', {'ISBN': pk,})
				.done(function(data) {
					self.check_inout(data['data'].id, 'check_out')
				})
				.fail(function(xhr, result, statusText){
					alertmessage('error', xhr.message)
				})

			},
			check_inout: function (pk, action) {
				let self = this

				rest_aj_send('post', '/ebookSystem/api/libraryrecords/' +pk +'/action/check_inout/', {'action': action,})
				.done(function(data) {
					let message = ''
					if(action==='check_in'){
						message = '成功歸還書籍'
						alertmessage('success', message)
						.done(function() {
							window.location.reload()
						})
					}
					if(action==='check_out'){
						message = '成功借閱書籍'
						alertmessage('success', message)
					}
				})
				.fail(function(xhr, result, statusText){
					alertmessage('error', xhr.message)
				})

			},
		},
	}
</script>