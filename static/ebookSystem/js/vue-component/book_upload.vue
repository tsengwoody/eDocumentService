<template>
	<div>
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
						<font style="color:red">*</font>{{ value.show }}：
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
							>{{ item.name }}</option>
						</select>
					</div>
				</template>
				<template v-else>
					<div class="col-sm-3">
						<div
							v-for="item in org_categorys"
							v-if="org_id==item.id"
						>{{ item.name }}</div>
					</div>
				</template>
			</div> 

			<div class="form-group">
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
							>{{ category.name }}</option>
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
			'bookinfo_search': components['bookinfo_search'],
		},
		data(){
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
			loading(){
				if(this.mode=='search') return 'inline-block'
				else if(this.mode=='input') return 'none'
				else return 'none';
			},
			url(){
				if(this.format=='epub' || this.format=='txt') return '/ebookSystem/api/books/action/upload/'
				else if(this.format=='self') return '/ebookSystem/api/books/action/create/'
			},
		},
		mounted(){
			this.get_org_category();
			this.org_id=user.org;
		},
		methods: {
			get_org_category(){
				genericUserAPI.organizationRest.list()
				.then(res => {
					_.each(res.data, (o) => {
						let org_category = {
							'id': o.id,
							'name': o.name,
							'categorys': [],
						}

						ebookSystemAPI.categoryRest.filter({'org_id': o.id})
						.then(res => {
							_.each(res.data, (c) => {
								let temp = {
									'id': c.id,
									'name': c.name,
								}
								org_category.categorys.push(temp)
							})
						})
						.catch(res => {
							alertmessage('error', o2j(res.response.data));
						})
						this.org_categorys.push(org_category)
					})
				})
				.catch(res => {
					alertmessage('error', o2j(res.response.data));
				})

			},
			search_ISBN_info(){
				if(binstr(this.search_ISBN, '-')){
					alertmessage('error', 'ISBN格式不能含有「-」')
					return -1;
				}
				if(this.search_ISBN.length!==10 && this.search_ISBN.length!==13){
					alertmessage('error', 'ISBN長度錯誤')
					return -1;
				}

				this.mode = 'search';

				Promise.all([
					ebookSystemAPI.bookInfoAction.isbn2bookinfo({ISBN: this.search_ISBN, source: 'NCL'}),
					//ebookSystemAPI.bookInfoAction.isbn2bookinfo({ISBN: this.search_ISBN, source: 'douban'}),
				])
				.then(res => {
					let result = [];
					if(res[0].data.bookinfo.ISBN){
						result = res[0].data.bookinfo;
						alertmessage('success', '查詢成功');
					}
					else {
						console.log('success search but not found')
						throw('not found');
					}

					this.search_ISBN = result['ISBN']; //若查詢ISBN10會自動轉ISBN13，故要重新更新
					_.each(this.temp, (v, k) => {
						this.temp[k].value = result[k];
					})
				})
				.catch(res => {
					console.log(JSON.stringify(res))
					alertconfirm('查無書籍資料，是否手動輸入？')
					.done(() => {
						_.each(this.temp, (v, k) => {
							this.temp[k].value = '';
							if(k==='ISBN'){
								this.temp[k].value = this.search_ISBN;
							}
							else if(k==='source'){
								this.temp[k].value = 'other';
							}
							else {
								this.temp[k].readonly = false;
							}
						})
						this.temp['source'].value = 'other';
					})
				})
				.finally(() => {
					this.mode = 'input';
				})
			},
			search_ISBN_info_more(data){
				let result = data;
				this.search_ISBN = result['ISBN']; //若查詢ISBN10會自動轉ISBN13，故要重新更新
				_.each(this.temp, (v, k) => {
					this.temp[k].value = result[k];
				})
			},
			create(){
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
				_.each(this.temp, (v, k) => {
					if(!(v.value==='')){
						transferData[k] = v.value
					}
				})

				ebookSystemAPI.bookInfoAction.createUpdate(transferData)
				.then(res => {
					let transferData = {
						ISBN: this.temp['ISBN'].value,
						org_id: this.org_id,
						category_id: this.category_id,
						format: this.format,
						fileObject: fileObject,
					}
					rest_aj_upload(this.url, transferData)
					.done((data) => {
						alertmessage('success', '成功更新資料(檔案)' +data['message'])
					})
					.fail((data) => {
						alertmessage('error', '失敗更新資料(檔案)' +data['message'])
					})
				})
				.catch(res => {
					alertmessage('error', o2j(res.response.data));
				})

			},
		},
	}

</script>