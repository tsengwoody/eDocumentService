<template>
	<div>
		<h2>公告內容</h2>
		<div class="form-horizontal">
			<div class="form-group">
				<label for="id_category" class="control-label col-sm-1"><font style="color:red">*</font>類別</label>
				<div class="col-sm-11">
					<div v-if="mode=='read'" class="panel panel-default" style="margin:0px; padding:5px 10px;">{{ announcement.category }}</div>
					<template v-if="mode=='write'">
						<select
							v-if="user.org=='1'"
							class="form-control"
							v-model="announcement.category"
						>
							<option value="平台消息">平台消息</option>
							<option value="天橋說書">天橋說書</option>
							<option value="新書推薦">新書推薦</option>
							<option value="志工快訊">志工快訊</option>
							<option value="校園公告">校園公告</option>
							<option value="校園平台消息">校園平台消息</option>
						</select>
					</template>
				</div>
			</div>
		
			<div class="form-group">
				<label for="id_title" class="control-label col-sm-1"><font style="color:red">*</font>標題</label>
				<div class="col-sm-11">
					<div v-if="mode=='read'" class="panel panel-default" style="margin:0px; padding:5px 10px;">{{ announcement.title }}</div>
					<template v-if="mode=='write'">
						<input v-model="announcement.title" class="form-control" type="text"/>
					</template>
				</div>
			</div>
		
			<div class="form-group">
				<label for="id_content" class="control-label col-sm-1"><font style="color:red">*</font>內容</label>
				<div class="col-sm-11">
					<div v-if="mode=='read'" v-html="announcement.content" class="panel panel-default" style="margin:0px; padding:5px 10px;"></div>
					<div v-if="mode=='write'">
						<editor
							v-model="announcement.content"
							:init="tinymce_init">
						</editor>
					</div>
				</div>
			</div>
		</div>
		
		<h2>附件檔案</h2>
		<file_manager
			:url="url +'resource/attachment/'"
			:permission="{
				'create': {'is_supermanager': true,},
				'read': {'is_all': true,},
				'update': {'is_supermanager': true,},
				'delete': {'is_supermanager': true,},
			}"
		></file_manager>
		<div class="form-group">        
			<div class="col-sm-offset-1 col-sm-11">
	
				<button
					v-if="mode=='read'"
					class="btn btn-primary"
					onclick="window.location='/routing/genericUser/announcement_list/'"
				>返回公告列表</button>
				<template v-if="user.is_manager===true">
					<button
						v-if="mode=='read'"
						@click="write_mode()"
						class="btn btn-primary"
					>進行修改</button>
					<button
						v-if="mode=='write'"
						@click="update()"
						class="btn btn-primary"
					>儲存</button>
					<button
						v-if="mode=='write'"
						@click="cancel()"
						class="btn btn-primary"
					>取消</button>
					<button
						v-if="mode=='write'"
						@click="deletes()"
						class="btn btn-danger"
					>刪除</button>
				</template>
	
			</div>
		</div>

	</div>
</template>

<script>
	module.exports = {
		components: {
			'editor': Editor,
			'file_manager': components['file_manager'],
		},
		data(){
			return {
				pk: '',
				announcement: {},
				url: '',
				mode: 'read', //read or write
				attachment_name: '',
				tinymce_init: {
					selector: "#id_content",
					language:"zh_TW",
					plugins: ['advlist autolink lists link image charmap print preview hr anchor pagebreak', 'searchreplace wordcount visualblocks visualchars code fullscreen', 'insertdatetime media nonbreaking save table contextmenu directionality', 'emoticons template paste textcolor colorpicker textpattern imagetools codesample toc'],
					toolbar: 'undo redo | insert | styleselect | bold italic | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | link image | print preview media | forecolor backcolor emoticons | codesample',
				},
			}
		},
		metaInfo: {
			title: '公告內容',
		},
		mounted(){
			let pk = window.location.pathname.split('/')
			this.pk = pk[pk.length-2]

			genericUserAPI.announcementRest.read(this.pk)
			.then(res => {
				this.announcement = res.data;
			})
			.catch(res => {
				alertmessage('error', o2j(res.response.data));
			})

		},
		methods: {
			read_mode(){
				this.mode = 'read'
			},
			write_mode(){
				this.mode = 'write'
			},
			update(){
				genericUserAPI.announcementRest.partialupdate(this.pk, this.announcement)
				.then(res => {
					alertmessage('success', '成功修改公告')
					.done(() => {
						this.mode = 'read'
					})
				})
				.catch(res => {
					alertmessage('error', o2j(res.response.data));
				})
			},
			cancel(){
				genericUserAPI.announcementRest.read(this.pk)
				.then(res => {
					this.announcement.category = res.data.category;
					this.announcement.title = res.data.title;
					this.announcement.content = res.data.content;
				})
				this.mode = 'read'
			},
			deletes(){
				alertconfirm('是否確定刪除公告?')
				.done(() => {
					genericUserAPI.announcementRest.delete(this.pk)
					.then(res => {
						alertmessage('success', '成功刪除公告')
						.done(() => {
							window.location='/routing/genericUser/announcement_list/';
						})
					})
					.catch(res => {
						alertmessage('error', o2j(res.response.data));
					})
				})
			},
		},
	}
</script>