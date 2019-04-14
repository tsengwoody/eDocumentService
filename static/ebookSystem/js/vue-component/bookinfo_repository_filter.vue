<template>
	<div id="bookinfo_repository_filter">
		<table-div :datas="datas" :header="header">
			<template slot="action" slot-scope="props">
				<button class="btn btn-default" @click="check_create(props.item)">借閱</button>
				<a class="btn btn-default" role="button"
					:href="'/ebookSystem/library_origin_view?ISBN=' +props.item"
					target="_blank" title="閱讀(另開新視窗)"
				>閱讀</a>
				<button class="btn btn-default"
					@click="
						feedback_id = props.item;

						$refs[id].open('bookinfo_repository_filter');
					">回報</button>
			</template>
		</table-div>
		<modal :id_modal="id" :size="'normal'" :ref="id">
			<template slot="header">
				<h4 class="modal-title">書籍 {|{ feedback_id }|} 回報</h4>
			</template>
			<template slot="body">
				<h5>回報內容:</h5>
				<textarea class="feedback" 
					v-model="feedback_content"
				></textarea>
			</template>
			<template slot="footer">
				<button
					class="btn btn-default"
					@click="$refs[id].close()"
				>取消</button>
				<button
					class="btn btn-default"
					@click="feedback()"
				>回報</button>
			</template>
		</modal>
	</div>
</template>

<script>

	module.exports = {
		props: ['header', 'datas',],
		components: {
			'modal': components['modal'],
			'table-div': components['table-div-filter'],
		},
		data: function(){
			return {
				id: Math.floor(Math.random() * 100000000).toString(),
				feedback_id: '',
				feedback_content: '',
			}
		},
		created: function () {
			let self = this
			self.clientg = new $.RestClient('/genericUser/api/')
			self.clientb = new $.RestClient('/ebookSystem/api/')
			self.clientb.add('books');
			self.clientb.books.addVerb('feedback', 'POST', {
				url: 'action/feedback/',
			});
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
			feedback: function () {
				let self = this
				let feedback_content = self.feedback_content
				self.clientb.books.feedback(self.feedback_id, {
					feedback_content: feedback_content,
				})
				.done(function(data) {
					alertmessage('success', '成功回報資料')
				})
				.fail(function(xhr, result, statusText){
					alertmessage('error', xhr.responseText)
				})

			},
		},
	}
</script>

<style>
.feedback {
	width: fill-available; 
	width: -webkit-fill-available; 
	height: 200px;
	color:  #4d4d4d;
	font-size: 1.2em;
}
</style>