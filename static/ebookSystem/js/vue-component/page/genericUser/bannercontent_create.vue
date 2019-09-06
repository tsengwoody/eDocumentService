<template>
	<div id="id_bannercontent_create" class="container">
		<h2>管理首頁 Banner</h2>
		<div class="row">
			<div class="col-sm-3 col-md-3">
				<div class="panel-group">
					<div class="panel panel-default">
						<div class="panel-heading">
							<h4 class="panel-title">
								<span class="glyphicon glyphicon-folder-close"></span>&nbsp;&nbsp;Banner
							</h4>
						</div>
						<div class="panel-collapse">
							<ul class="list-group">
								<li class="list-group-item"><a
									v-on:click="read(-1)"
									href='#'
									>新增</a></li>
								<li class="list-group-item" v-for="(item, index) in items"><a 
									v-on:click="read(index)"
									href='#'
								>{{ index+1 }}. {{ item.title }}</a></li>
							</ul>
						</div>
					</div>
				</div>
			</div>
			<div class="col-sm-9 col-md-9">
				<div v-if="index!=-1" style='float: right;'>
					<button type="button" class="btn btn-default" v-if="mode=='read'" v-on:click="change_mode">編輯</button>
					<button type="button" class="btn btn-default" v-if="mode=='write'" v-on:click="change_mode">檢視</button>
				</div>
				<div v-if="mode=='read'">
					<p class="h5"><strong>摘要文字</strong></p>
					<p>{{ temp.title }}</p>
					<p class="h5"><strong>圖片內容</strong></p>
					<img
						v-if="index!=-1"
						:alt="temp.title"
						:src="'/genericUser/api/bannercontents/' +temp.id +'/resource/cover/image/'"
						style="height: 480px;width:940px"
					>
					<br>
					<p class="h5"><strong>詳細說明</strong></p>
					<p v-html="markdown2html(temp.content)"></p>
				</div>
				<div v-if="mode=='write'">
					<form>
						<div class="form-group">
							<label for="id_title">摘要文字</label>
							<input id="id_title" v-model="temp.title" class="form-control" placeholder="title">
						</div>
						<p class="h5"><strong>圖片內容</strong></p>
						<img
							v-if="index!=-1"
							v-bind:alt="temp.title"
							v-bind:src="url +`resource/cover/image/`"
							style="height: 480px;width:940px"
						>
						<br><br>
						<div class="form-group">
							<label for="id_content">詳細說明</label>
							<textarea class="form-control" id="id_content" v-model="temp.content" rows="3" placeholder="content"></textarea>
						</div>
						<div class="form-group">
							<label for="id_url">連結網址</label>
							<input class="form-control" id="id_url" v-model="temp.url" rows="3" placeholder="url"></input>
						</div>
						<div class="form-group">
							<label for="id_cover">上傳圖檔</label>
							<input type="file" class="form-control-file" id="id_cover" name="cover"/>
						</div>
					</form>
					<div>
						<button class="btn btn-primary" v-if="index==-1" v-on:click="create()">新增</button>
						<button class="btn btn-primary" v-else v-on:click="update()">更新</button>
						<button class="btn btn-danger" v-if="index!=-1" v-on:click="del()">刪除</button>
					</div>
				</div>
				
			</div>
		</div>
	</div>
</template>

<script>
	module.exports = {
		data(){
			return {
				website: 'all',
				'mode': 'write', //read or write
				'items': [],
				'index': -1,
				'temp': {
					'id': '',
					'title': '',
					'content': '',
					'order': '',
					'url': '',
				},
			}
		},
		computed: {
		},
		metaInfo: {
			title: '管理首頁 Banner',
		},
		mounted(){
			website = localStorage.getItem('nav_mode');
			if (website){
				this.website = website;
			}
			this.list()
		},
		methods: {
			upload(id){
				let fileCover = document.getElementById('id_cover');
				fileObject = fileCover.files[0]
				if(iser(fileObject)){
					alertmessage('error', '檔案尚未選擇')
					return -1
				}
				let url_resource = '/genericUser/api/bannercontents/' +id +'/resource/cover/image/'
				rest_aj_upload(url_resource, {'object': fileCover.files[0]})
				.done((data) => {
					alertmessage('success', '成功更新資料(檔案)' +data['message'])
					this.clear()
				})
				.fail((data) => {
					alertmessage('error', '失敗更新資料(檔案)' +data['message'])
				})
			},
			clear(){
				this.index = -1;
				this.temp = {
					'id': -1,
					'title': '',
					'content': '',
					'order': -1,
					category: this.website,
				}
			},
			list(){
				genericUserAPI.bannerContentRest.filter({category: this.website})
				.then(res => {
					this.items = res.data;
					this.read(this.index);
				})
			},
			create(){
				genericUserAPI.bannerContentRest.create(this.temp)
				.then(res => {
						let fileCover = document.getElementById('id_cover');
						fileObject = fileCover.files[0]
						if(!iser(fileObject)){
							this.upload(res.data.id)
						}
						else {
							alertmessage('success', '成功建立資料')
						}
					this.list();
				})
				.catch(res => {
					alertmessage('error', o2j(res.response.data));
				})
			},
			read(index) {
				this.index = index;
				if(index==-1){
					this.mode = 'write';
					this.clear();
				}
				else{
					this.mode = 'read';
					this.temp = this.items[index];
				}
			},
			update(){
				genericUserAPI.bannerContentRest.update(this.temp.id, this.temp)
				.then(res => {
						let fileCover = document.getElementById('id_cover');
						fileObject = fileCover.files[0]
						if(!iser(fileObject)){
							this.upload(res.data.id)
						}
						else {
							alertmessage('success', '成功更新資料')
						}
					this.list();
				})
				.catch(res => {
					alertmessage('error', o2j(res.response.data));
				})
			},
			del(){
				genericUserAPI.bannerContentRest.delete(this.temp.id)
				.then(res => {
					this.index = -1;
					this.list();
					alertmessage('success', '已刪除');
				})
				.catch(res => {
					alertmessage('error', o2j(res.response.data));
				})
			},
			change_mode(){
				if(this.mode=='read'){ this.mode = 'write' }
				else if(this.mode=='write'){ this.mode = 'read' }
			},
			markdown2html(text){
				let converter = new showdown.Converter()
				html = converter.makeHtml(text)
				return html
			},
		},
	}
</script>