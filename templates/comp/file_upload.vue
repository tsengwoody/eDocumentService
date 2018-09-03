{% include 'comp/table-div.vue' %}
<template id="file_upload">
	<modal id_modal="fum">
		<template slot="header">
			<h4 class="modal-title">檔案上傳</h4>
		</template>
		<template slot="body">
			<div v-if="!(mode==='delete')" class="form-group">
				<div>
					<label for="id_resource_name" class="control-label col-sm-1">檔案名稱：</label>
					<div v-if="mode==='create'" class="col-sm-11">
						<input
							id="id_resource_name"
							v-model="resource_name"
							type="text"
						>
					</div>
					<div v-if="mode==='update'" class="col-sm-11">
						{|{ resource_name }|}
					</div>

					<label class="control-label col-sm-1">檔案選擇：</label>
					<div class="col-sm-11">
						<input
							id="id_resource"
							type="file"
						>
					</div>
					<button
						@click="upload_resource()"
						class="btn btn-primary"
					>上傳</button>
				</div>
			</div>
			<div v-else>
				<p>確定要刪除文件？</p>
				<button
					class="btn btn-default"
					@click="delete_resource()"
				>刪除</button>
			</div>
		</template>
	</modal>
</template>
<script>
	Vue.options.delimiters = ['{|{', '}|}'];

	Vue.component('file_upload', {
		template: '#file_upload',
		props: ['url', 'resource_name',],
		data: function(){
			return {
				mode: '', //create / update / delete
			}
		},
		computed: {
		},
		mounted: function () {
			if(iser(this.resource_name)){
				this.change_mode('create')
			}
			else {
				this.change_mode('update')
			}
		},
		methods: {
			change_mode: function(mode){
				this.mode = mode
			},
			upload_resource: function(){
				let self = this

				let fileresource = document.getElementById('id_resource');
				fileresourceObject = fileresource.files[0]
				if(iser(fileresourceObject)){
					alertmessage('error', '尚未選擇上傳附件')
				}

				rest_aj_upload(self.url +self.resource_name +'/', {'object': fileresourceObject})
				.done(function(data) {
					self.$emit('change')
					alertmessage('success', '成功上傳檔案')
				})
				.fail(function(xhr, result, statusText){
					console.log(xhr)
					alertmessage('error', xhr.message)
				})

			},
			delete_resource: function(){
				let self = this
				rest_aj_send('delete', self.url +self.resource_name +'/', {})
				.done(function(data) {
					self.$emit('change')
					self.change_mode('create')
					alertmessage('success', '成功刪除檔案')
				})
				.fail(function(xhr, result, statusText){
					console.log(xhr)
					alertmessage('error', xhr.message)
				})
			},
		},
	})

</script>