<template>
	<div class="form-horizontal">
		<h3>公告發佈</h3>
		<div class="form-group">
			<label for="id_category" class="control-label col-sm-1"><font style="color:red">*</font>類別</label>
			<div class="col-sm-11">
				<select
					class="form-control"
					v-model="category"
				>
					<option value="">---------</option>
					<option value="平台消息">平台消息</option>
					<option value="天橋說書">天橋說書</option>
					<option value="新書推薦">新書推薦</option>
					<option value="志工快訊">志工快訊</option>
				</select>
			</div>
		</div>
	
		<div class="form-group">
			<label for="id_title" class="control-label col-sm-1"><font style="color:red">*</font>標題</label>
			<div class="col-sm-11">
				<input
					maxlength="30"
					class="form-control" 
					type=text
					placeholder="title"
					required
					v-model="title"
				>
			</div>
		</div>
	
		<div class="form-group">
			<label for="id_content" class="control-label col-sm-1"><font style="color:red">*</font>內容</label>
			<div class="col-sm-11">
				<editor v-model="content" :init="tinymce_init"></editor>
			</div>
			
		</div>
	
		<div class="form-group">        
			<div class="col-sm-offset-1 col-sm-11">
				<button type="button" class="btn btn-primary" @click="create()">發佈</button>
				<button type="button" class="btn btn-danger" @click="cancel()">取消</button>
			</div>
		</div>
	</div>
</template>

<script type="text/javascript">

	let tinymce_init = {
		selector: "#id_content",
		language:"zh_TW",
		plugins: ['advlist autolink lists link image charmap print preview hr anchor pagebreak', 'searchreplace wordcount visualblocks visualchars code fullscreen', 'insertdatetime media nonbreaking save table contextmenu directionality', 'emoticons template paste textcolor colorpicker textpattern imagetools codesample toc'],
		toolbar: 'undo redo | insert | styleselect | bold italic | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | link image | print preview media | forecolor backcolor emoticons | codesample'
	};

	module.exports = {
		data: function(){
			return {
				title: '',
				category: '',
				content: '',
				tinymce_init: tinymce_init,
			}
		},
		components: {
			'editor': Editor
		},
		computed: {
			transferData: function(){
				return {
					'title': this.title,
					'category': this.category,
					'content': this.content,
				}
			},
		},
		mounted: function(){
			document.title = '公告發佈'
		},
		methods: {
			cancel: function(){
				if(!isobjvalueer(this.transferData)){
					alertconfirm('已經填寫資料，是否確定取消?')
					.done(function(){
						//重新整理
						window.location.reload();
					})
				}
				else{
					//重新整理
					window.location.reload();
				}
			},
			create: function(){
				rest_aj_send('post', '/genericUser/api/announcements/', this.transferData)
				.done(function(data){
					alertmessage('success', '成功新建公告',)
					.done(function(){
						//重新整理
						window.location.replace('/routing/genericUser/announcement/' +data.data['id'] +'/')
					})
				})
				.fail(function(data){
				    alertmessage('error', data['message']);
				})
			}
		},
	}

</script>