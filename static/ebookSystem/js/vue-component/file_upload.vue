<template>
	<modal id_modal="fum">
		<template slot="header">
			<h4 class="modal-title">檔案上傳</h4>
		</template>
		<template slot="body">
			<div class="form-horizontal">
				<div v-if="!(mode==='delete')">
					<div class="form-group">
						<label for="id_resource_name" class="control-label col-sm-3">檔案名稱：</label>
						<div v-if="mode==='create'" class="col-sm-3">
							<input
								id="id_resource_name"
								class="form-control"
								v-model="resource_name"
								type="text"
							>
						</div>
						<div v-if="mode==='update'" class="col-sm-3 likebtn">
							{|{ resource_name }|}
						</div>
					</div>
					<div class="form-group">
						<label class="control-label col-sm-3">檔案選擇：</label>
						<div class="col-sm-6">
							<input
								id="id_resource"
								type="file"
							>
						</div>
					</div>
				</div>
				<div v-else>
					<h3>確定要刪除文件？</h3>
				</div>
			</div>
		</template>
		<template slot="footer">
			<button v-if="!(mode==='delete')"
				ref="up"
				@click="upload_resource();"
				class="btn btn-default"
			>上傳</button>

			<button v-else
				ref="del"
				class="btn btn-default"
				@click="delete_resource();"
			>刪除</button>

			<button
				onclick="closeDialog(this)"
				class="btn btn-default"
			>關閉</button>
		</template>
	</modal>
</template>
<script>
	Vue.options.delimiters = ['{|{', '}|}'];

	function getExt(filename){
		// 依照名稱找副檔名
		var ext = filename.split('.').pop();
	    if(ext == filename) return '';
	    return ext;
	}	

	module.exports = {
		props: ['url', 'resource_name',],
		components: {
			'modal': components['modal'],
		},
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
				let self = this;
				let fileresource = document.getElementById('id_resource');
				let fileresourceObject = fileresource.files[0];
				let resource_name = self.resource_name;

				let fileExtension = '';
				if(!iser(fileresourceObject)){
					fileExtension = getExt(fileresourceObject.name);
				} else {
					alertmessage('error', '尚未選擇上傳附件')
					return false;
				}

				let nameExtension = '';
				if(resource_name) {
					nameExtension = getExt(resource_name);
				} else {
					alertmessage('error', '輸入檔案名稱')
					return false;
				}

				if(fileExtension && nameExtension) {
					if(fileExtension !== nameExtension) {
						alertconfirm('檔案附檔名不一致，是否自動加上副檔名?')
						.done(function(){
							self.resource_name = resource_name + '.' + fileExtension;
							self.upload_file(self.url +self.resource_name +'/', {'object': fileresourceObject})
						})
					} else {
						self.upload_file(self.url +self.resource_name +'/', {'object': fileresourceObject})
					}
				} 
				else if (fileExtension && !nameExtension) {
					alertconfirm('檔案名稱未包含附檔名，確定後系統將自動加入')
					.done(function(){
						self.resource_name = resource_name + '.' + fileExtension;
						self.upload_file(self.url +self.resource_name +'/', {'object': fileresourceObject})
					})
				} else {
					self.upload_file(self.url +self.resource_name +'/', {'object': fileresourceObject})
				}
			},
			upload_file: function(path, object){
				let self = this;

				rest_aj_upload(path, object)
				.done(function(data) {
					self.$emit('change')
					alertmessage('success', '成功上傳檔案')
					.done(function(){
						closeDialog(self.$refs.up);
					})
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
					// self.change_mode('create')
					alertmessage('success', '成功刪除檔案')
					.done(function(){
						closeDialog(self.$refs.del);
					})
				})
				.fail(function(xhr, result, statusText){
					console.log(xhr)
					alertmessage('error', xhr.message)
				})
			},
		},
	}

</script>