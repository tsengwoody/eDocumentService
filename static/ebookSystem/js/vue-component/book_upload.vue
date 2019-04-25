<template>
	<div>
		{|{ org_id }|}
		{|{ category_id }|}
		<h3 v-if="format!='self'"><legend>電子檔上傳</legend></h3>
		<h3 v-else><legend>掃描檔上傳</legend></h3>
		<div class="form-horizontal">
			<div class="form-group">
				<label class="control-label col-sm-2" for="id_search_ISBN"><font style="color:red">*</font>ISBN:</label>
				<div class="col-sm-3">
					<input type="text" class="form-control" id="id_search_ISBN" name="ISBN"  placeholder="請輸入正確的ISBN(10碼或13碼）"
						pattern="(ISBN[-]*(1[03])*[ ]*(: ){0,1})*(([0-9Xx][- ]*){13}|([0-9Xx][- ]*){10})"
						v-model="search_ISBN"
					autofocus required>
				</div>
					<input id="get_isbn" type="button" class="btn btn-default" value="取得書籍資訊"
						v-bind:disabled="mode=='search'"
						v-on:click="search_ISBN_info()"
					>
					<img src="/static/ebookSystem/img/load.gif" v-bind:style="{ display:loading }" width="30px" height="30px" id="id_get_isbn_load_icon" />
					<button
						class="btn btn-default"
						@click="openDialog('bis', this);"
					>更多查詢方式</button>
					<a type="button" class="btn btn-default" href="http://isbn.ncl.edu.tw/NCL_ISBNNet/H30_SearchBooks.php?PHPSESSID=3ovphpac0m41ducm3iiak2sfe5&Pact=DisplayAll" target="_blank" id="to_ISBNNet" title="開啟新視窗">國家圖書館書目資料查詢</a>
					<button
						style="display: none;"
						class="btn btn-default"
						@click=""
					>手動輸入</button>
			</div> 
			<div v-for="(value, key) in temp">
				<div class="form-group">
					<label class="control-label col-sm-2"
						v-bind:for="'id_' +key"
					>
						<font style="color:red">*</font>{|{ value.show }|}：
					</label>
					<div class="col-sm-3">
						<input type="text" grp="changemode" class="form-control"
							v-bind:id="'id_' +key"
							v-bind:name="key"
							v-model:value="temp[key].value"
							v-bind:readonly="value.readonly"
						>
					</div>
				</div>
			</div>
			<template v-if="format!='self'">
				<div class="form-group">
					<label class="control-label col-sm-2" for="id_format">格式：</label>
					<div class="col-sm-3">
						<select
							class="form-control"
							v-model="format"
							id="id_format" name="format" required
						>
							<option value="" selected="selected">---------</option>
							<option value="txt">txt</option>
							<option value="epub">epub</option>
						</select>
					</div>
				</div> 
			</template>

			<div class="form-group">
				<label class="control-label col-sm-2" for="id_org">單位：</label>
				<template v-if="user.is_supermanager">
					<div class="col-sm-3">
						<select
							class="form-control"
							v-model="org_id"
							id="id_org" name="org" required
							@change="category_id=''"
						>
							<option
								v-for="item in org_categorys"
								:value="item.id"
							>{|{ item.name }|}</option>
						</select>
					</div>
				</template>
				<template v-else>
					<div class="col-sm-3">
						<div
							v-for="item in org_categorys"
							v-if="org_id==item.id"
						>{|{ item.name }|}</div>
					</div>
				</template>
				<label class="control-label col-sm-2" for="id_category">類別：</label>
				<div class="col-sm-3">

					<template
						v-for="item in org_categorys"
						v-if="org_id==item.id"
					>
						<select
							class="form-control"
							v-model="category_id"
							id="id_category" name="category"
						>
							<option value="">-----請選擇-----</option>
							<option
								v-for="category in item.categorys"
								:value="category.id"
							>{|{ category.name }|}</option>
						</select>
					</template>
				</div>

			</div> 

			<div class="form-group">
				<label class="control-label col-sm-2" for="id_fileObject">文件：</label>
				<div class="col-sm-3">
					<input class="form-control-file" id="id_fileObject" name="fileObject" type="file" required />		  
				</div>
			</div> 

			<div class="form-group row">
				<div class="col-sm-offset-2 col-sm-10">
					<input v-on:click="create()" type="button" class="btn btn-primary upload" value="送出" id="send_id">
					<input type="reset" class="btn btn-danger" value="重置">
				</div>
			</div>
		</div>
	
	
	
		<bookinfo_search
			v-on:bookinfo-out="search_ISBN_info_more($event)"
			ref="vo_bis"
		></bookinfo_search>
	
	</div>
</template>
<script>
	module.exports = {
		props: ['format',],
		components: {
			'bookinfo_search': httpVueLoader('/static/ebookSystem/js/vue-component/bookinfo_search.vue')
		},
		data: function(){
			return {
				mode:'input', //input or search
				search_ISBN: '',
				temp: {
					'ISBN': {
						'value': '',
						'show': 'ISBN',
						'readonly': true,
					},
					'bookname': {
						'value': '',
						'show': '書名',
						'readonly': true,
					},
					'author': {
						'value': '',
						'show': '作者',
						'readonly': true,
					},
					'house': {
						'value': '',
						'show': '出版社',
						'readonly': true,
					},
					'date': {
						'value': '',
						'show': '出版日期',
						'readonly': true,
					},
					'bookbinding': {
						'value': '',
						'show': '裝訂冊數',
						'readonly': true,
					},
					'chinese_book_category': {
						'value': '',
						'show': '中文圖書分類',
						'readonly': true,
					},
					'order': {
						'value': '',
						'show': '版次',
						'readonly': true,
					},
					'source': {
						'value': '',
						'show': '來源',
						'readonly': true,
					},
				},
				org_id: '',
				category_id: '',
				org_categorys: [],
			}
		},
		computed: {
			loading: function(){
				if(this.mode=='search') return 'inline-block'
				else if(this.mode=='input') return 'none'
				else return 'none';
			},
			url: function(){
				if(this.format=='epub' || this.format=='txt') return '/ebookSystem/api/books/action/upload/'
				else if(this.format=='self') return '/ebookSystem/api/books/action/create/'
			},
		},
		mounted: function () {
			let self = this
			self.clientb = new $.RestClient('/ebookSystem/api/');
			self.clientb.add('bookinfos');
			self.clientb.add('categorys');
			self.clientb.addVerb('bookinfos_create_update', 'POST', {
				url: 'bookinfos/action/create_update/',
			});
			self.clientg = new $.RestClient('/genericUser/api/');
			self.clientg.add('organizations');
			self.get_org_category()
			self.org_id=user.org
		},
		methods: {
			get_org_category: function(){
				let self = this
				self.clientg.organizations.read()
				.done(function(data) {
					_.each(data, function(o){
						let org_category = {
							'id': o.id,
							'name': o.name,
							'categorys': [],
						}

						self.clientb.categorys.read({'org_id': o.id})
						.done(function(data) {
							_.each(data, function(c){
								let temp = {
									'id': c.id,
									'name': c.name,
								}
								org_category.categorys.push(temp)
							})
						})
						.fail(function(xhr, result, statusText){
							alertmessage('error', xhr.responseText)
						})
						self.org_categorys.push(org_category)
					})
				})
				.fail(function(xhr, result, statusText){
					alertmessage('error', xhr.responseText)
				})

			},
			search_ISBN_info: function(){
				if(binstr(this.search_ISBN, '-')){
					alertmessage('error', 'ISBN格式不能含有「-」')
					return -1;
				}
				if(this.search_ISBN.length!==10 && this.search_ISBN.length!==13){
					alertmessage('error', 'ISBN長度錯誤')
					return -1;
				}

				let self = this
				self.mode = 'search';

				self.aj_ncl_douban_ISBN(this.search_ISBN)
				.done(function(data){
					alertmessage('success', '查詢成功');
					self.search_ISBN = data['ISBN']; //若查詢ISBN10會自動轉ISBN13，故要重新更新
					_.each(self.temp, function(v, k){
						self.temp[k].value = data[k];
					})
				})
				.fail(function(data){
					alertconfirm('查無書籍資料，是否手動輸入？')
					.done(function(){
						_.each(self.temp, function(v, k){
							self.temp[k].value = '';
							if(k==='ISBN'){
								self.temp[k].value = self.search_ISBN;
							}
							else if(k==='source'){
								self.temp[k].value = 'other';
							}
							else {
								self.temp[k].readonly = false;
							}
						})
						self.temp['source'].value = 'other';
					})
				})
				.always(function(){
					self.mode = 'input';
				})
			},
			aj_ncl_douban_ISBN: function(value){
				//用ISBN查找[全國新書資訊網]與[豆瓣]書籍資訊，並以[全國新書資訊網]優先
				let self = this
				//df
				let df = GenDF();
				let ncl_data = [];
				let ncl_df = GenDF()
				let douban_data = [];
				let douban_df = GenDF()
				rest_aj_send('post', '/ebookSystem/api/bookinfos/action/isbn2bookinfo/', {'ISBN': value, 'source':'NCL',})
				.done(function (data) {
					ncl_data = data['data'].bookinfo
					douban_df.resolve(douban_data);
				})
				.fail(function(xhr, result, statusText){
					console.log(xhr)
				})
				.always(function () {
					ncl_df.resolve(ncl_data);
				})
				rest_aj_send('post', '/ebookSystem/api/bookinfos/action/isbn2bookinfo/', {'ISBN': value, 'source':'douban',})
				.done(function (data) {
					douban_data = data['data'].bookinfo
				})
				.fail(function(xhr, result, statusText){
					console.log(xhr)
				})
				.always(function () {
					douban_df.resolve(douban_data);
				})
				//when
				$.when(ncl_df, douban_df)
				.done(function (data1, data2) {
					if(!iser(data1.ISBN)){
						df.resolve(data1);
					}
					else if(!iser(data2.ISBN)){
						df.resolve(data2);
					}
					else {
						df.reject('無書籍資料');
					}
				})
				return df;
			},
			search_ISBN_info_more: function(data){
				let self = this
				self.search_ISBN = data['ISBN']; //若查詢ISBN10會自動轉ISBN13，故要重新更新
				self.temp['ISBN'].value = data['ISBN'];
				self.temp['bookname'].value = data['bookname'];
				self.temp['author'].value = data['author'];
				self.temp['date'].value = data['date'];
				self.temp['house'].value = data['house'];
				self.temp['bookbinding'].value = data['bookbinding'];
				self.temp['chinese_book_category'].value = data['chinese_book_category'];
				self.temp['order'].value = data['order'];
				self.temp['source'].value = data['source'];
			},
			create: function(){
				let self = this;

				// 確認有選擇類型
				if(iser(this.format)){
					alertmessage('error', '類型尚未選擇')
					return -1
				}
				let fileObject = document.getElementById('id_fileObject').files[0]
				// 確認有選擇檔案
				if(iser(fileObject)){
					alertmessage('error', '檔案尚未選擇')
					return -1
				}

				let transferData = {}
				_.each(self.temp, function(v, k){
					if(!(v.value==='')){
						transferData[k] = v.value
					}
				})

				self.clientb.bookinfos_create_update(transferData)
				.done(function(data){
					let transferData = {
						ISBN: self.temp['ISBN'].value,
						org_id: self.org_id,
						category_id: self.category_id,
						format: self.format,
						fileObject: fileObject,
					}
					rest_aj_upload(self.url, transferData)
					.done(function(data) {
						alertmessage('success', '成功更新資料(檔案)' +data['message'])
					})
					.fail(function(data){
						alertmessage('error', '失敗更新資料(檔案)' +data['message'])
					})
				})
				.fail(function(xhr, result, statusText){
					alertmessage('error', xhr.responseText)
				})

			},
		},
	}

</script>