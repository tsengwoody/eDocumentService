<template>
	<modal id_modal="bis">
		<template slot="header">
			<h4 class="modal-title">更多查詢方式</h4>
		</template>
		<template slot="body">
			<div v-if="mode==='request'">
				<ul class="nav nav-tabs">
					<li class="active" name="divmodal_FindBook_tab_grp" mode="easy">
						<a @click="source='intergrate'" href="#divmodal_FindBook_tab_easy" data-toggle="tab" aria-expanded="true">綜合查詢</a>
					</li>
					<li name="divmodal_FindBook_tab_grp" mode="adv">
						<a @click="source='ncl'" href="#divmodal_FindBook_tab_adv" data-toggle="tab" aria-expanded="false">國圖查詢</a>
					</li>
				</ul>
				<div class="tab-content">
					<div id="divmodal_FindBook_tab_easy" class="tab-pane active">
						<div style="margin:20px 0px 10px 0px;">輸入書籍ISBN或書名進行查詢：</div>
						<input v-model="intergrate_value" type="text" class="form-control">
					</div>
					<div id="divmodal_FindBook_tab_adv" class="tab-pane">
						<div style="margin:20px 0px;">輸入書籍相關資訊與條件進行查詢：</div>
						<div class="form-group form-inline">
							<span style="display:inline-block; text-align:right; width:100px; margin-right:10px;">尋找：</span>
							<span>在</span>
							<select v-model="ncl_query['FO_SearchField0']" class="form-control">
								<option value="Title" selected="">書名</option>
								<option value="Author">作者</option>
								<option value="PublisherShortTitle">出版者</option>
								<option value="SubjHeading">標題(主題詞)</option>
								<option value="SerialTitle">叢書名</option>
								<option value="ClassNo">分類號</option>
								<option value="ISBN">ISBN</option>
								<option value="Date_Sales">確認出版年月</option>
								<option value="PubMonth_Pre">預計出版年月</option>
							</select>
							<span>為</span>
							<input v-model="ncl_query['FO_SearchValue0']" class="form-control" type="text">
						</div>
						<div class="form-group form-inline">
							<select v-model="ncl_query['FO_SchRe1ation1']" class="form-control" style="width:100px; margin-right:10px;">
								<option value="AND" selected>與(AND)</option>
								<option value="OR">或(OR)</option>
								<option value="NOT">非(NOT)</option>
							</select>
							<span>在</span>
							<select v-model="ncl_query['FO_SearchField1']" class="form-control">
								<option value="Title" selected="">書名</option>
								<option value="Author">作者</option>
								<option value="PublisherShortTitle">出版者</option>
								<option value="SubjHeading">標題(主題詞)</option>
								<option value="SerialTitle">叢書名</option>
								<option value="ClassNo">分類號</option>
								<option value="ISBN">ISBN</option>
								<option value="Date_Sales">確認出版年月</option>
								<option value="PubMonth_Pre">預計出版年月</option>
							</select>
							<span>為</span>
							<input v-model="ncl_query['FO_SearchValue1']" class="form-control" type="text">
						</div>
						<div class="form-group form-inline">
							<select v-model="ncl_query['FO_SchRe1ation2']" class="form-control" style="width:100px; margin-right:10px;">
								<option value="AND" selected>與(AND)</option>
								<option value="OR">或(OR)</option>
								<option value="NOT">非(NOT)</option>
							</select>
							<span>在</span>
							<select v-model="ncl_query['FO_SearchField2']" class="form-control">
								<option value="Title" selected="">書名</option>
								<option value="Author">作者</option>
								<option value="PublisherShortTitle">出版者</option>
								<option value="SubjHeading">標題(主題詞)</option>
								<option value="SerialTitle">叢書名</option>
								<option value="ClassNo">分類號</option>
								<option value="ISBN">ISBN</option>
								<option value="Date_Sales">確認出版年月</option>
								<option value="PubMonth_Pre">預計出版年月</option>
							</select>
							<span>為</span>
							<input id="ncl_query['FO_SearchValue2']" class="form-control" type="text">
						</div>
					</div>
				</div>
			</div>
			<div v-if="mode==='loading'">
				<div>正在取得書籍資訊中</div>
			</div>
			<div v-if="mode==='response'">
				<h4>請由下列書籍清單中勾選欲上傳之書籍：</h4>
				<div id="divmodal_FindBook_page_pick_list" style="overflow-x:auto;"></div>
				<table-div :header="bookinfo_header" :datas="result">
					<template slot="check" slot-scope="props">
						<input type="radio" v-model="bookinfo_check" :value="props.item">
					</template>
				</table-div>
				<button
					@click="reset()"
					class="btn btn-primary"
				>重新查詢</button>
			</div>
		</template>
		<template slot="footer">
			<button class="btn btn-danger" onclick="closeDialog(this)">取消</button>
			<button
				v-if="mode==='request'"
				@click="FindBook()"
				class="btn btn-primary"
			>取得</button>
			<button
				v-if="mode==='response'"
				ref="cb"
				@click="bookinfo_out(); closeDialog($refs.cb);"
				class="btn btn-primary"
			>確定</button>
		</template>
	</modal>
</template>
<script>
	Vue.options.delimiters = ['{{', '}}'];

	module.exports = {
		props: [],
		components: {
			'table-div': components['table-div'],
			'modal': components['modal'],
		},
		data(){
			return {
				mode: 'request', //request, response
				source: 'intergrate', //intergrate, ncl, douban
				intergrate_value: '',
				default_ncl_query: {
					source: 'NCL',
					'FO_SchRe1ation0': 'Null',
					'FO_SearchField0': 'Title',
					'FO_SearchValue0': '',
					'FO_SchRe1ation1': 'OR',
					'FO_SearchField1': 'ISBN',
					'FO_SearchValue1': '',
					'FO_SchRe1ation2': 'OR',
					'FO_SearchField2': 'Author',
					'FO_SearchValue2': '',
				},
				ncl_query: {
					source: 'NCL',
					'FO_SchRe1ation0': 'Null',
					'FO_SearchField0': 'Title',
					'FO_SearchValue0': '',
					'FO_SchRe1ation1': 'OR',
					'FO_SearchField1': 'ISBN',
					'FO_SearchValue1': '',
					'FO_SchRe1ation2': 'OR',
					'FO_SearchField2': 'Author',
					'FO_SearchValue2': '',
				},
				default_douban_query: {
					source: 'douban',
					'search_query' :'',
				},
				douban_query: {
					source: 'douban',
					'search_query' :'',
				},
				bookinfo_header: {
					check: "勾選",
					"ISBN": "ISBN",
					"bookname": "書名",
					"bookbinding": "裝訂冊數",
					"order": "版次",
					"author": "作者",
					"house": "出版社",
					"date": "出版日期",
					"chinese_book_category": "圖書類號",
					"source" :"來源",
				},
				result: [],
				bookinfo_check: 0,
			}
		},
		methods: {
			intergrate(){
				let value = this.intergrate_value;

				// ncl
				let ncl_query = _.clone(this.default_ncl_query);
				ncl_query['FO_SearchValue0'] = value;
				ncl_query['FO_SearchValue1'] = value;
				// douban
				let douban_query = _.clone(this.default_douban_query);
				douban_query['search_query'] = value;

				this.mode = 'loading';
				Promise.all([
					ebookSystemAPI.bookInfoAction.key2bookinfo(ncl_query),
					ebookSystemAPI.bookInfoAction.key2bookinfo(douban_query),
				])
				.then(res => {
					let index = 0;
					_.each(res[0].data['bookinfo_list'], (v) => {
						this.result.push({
							"check": index,
							"ISBN": v['ISBN'],
							"bookname": v['bookname'],
							"bookbinding": v['bookbinding'],
							"order": v['order'],
							"author": v['author'],
							"house": v['house'],
							"date": v['date'],
							"chinese_book_category": v['chinese_book_category'],
							"source": v['source'],
						})
						index = index +1;
					})
					_.each(res[1].data['bookinfo_list'], (v) => {
						this.result.push({
							"check": index,
							"ISBN": v['ISBN'],
							"bookname": v['bookname'],
							"bookbinding": v['bookbinding'],
							"order": v['order'],
							"author": v['author'],
							"house": v['house'],
							"date": v['date'],
							"chinese_book_category": v['chinese_book_category'],
							"source": v['source'],
						})
						index = index +1;
					})
					this.mode = 'response';
					if (this.result.length === 0) {
						this.mode = 'request';
						alertmessage('error', '查無書籍資料');
					}
				})
				.catch(res => {
					this.mode = 'request';
					alertmessage('error', o2j(res));
				})
			},
			ncl(){
				this.mode = 'loading';
				ebookSystemAPI.bookInfoAction.key2bookinfo(this.ncl_query)
				.then(res => {
					let index = 0;
					_.each(res.data['bookinfo_list'], (v) => {
						this.result.push({
							"check": index,
							"ISBN": v['ISBN'],
							"bookname": v['bookname'],
							"bookbinding": v['bookbinding'],
							"order": v['order'],
							"author": v['author'],
							"house": v['house'],
							"date": v['date'],
							"chinese_book_category": v['chinese_book_category'],
							"source": v['source'],
						})
						index = index +1;
					})
					this.mode = 'response';
					if (this.result.length === 0) {
						this.mode = 'request';
						alertmessage('error', '查無書籍資料');
					}
				})
				.catch(res => {
					this.mode = 'request';
					alertmessage('error', o2j(res.response.data));
				})
			},
			FindBook(){
				if (this.source=== 'intergrate') {
					this.intergrate();
				}
				else if (this.source === 'ncl') {
					this.ncl();
				}
			},
			bookinfo_out() {
				this.$emit('bookinfo-out', this.result[this.bookinfo_check]);
			},
			reset(){
				this.mode = 'request'
				this.source = 'intergrate'
				this.intergrate_value = ''
				_.each(this.default_ncl_query, (v, k) => {
					this.ncl_query[k] = this.default_ncl_query[k]
				})
				_.each(this.default_douban_query, (v, k) => {
					this.douban_query[k] = this.default_douban_query[k]
				})
				this.result = []
				this.bookinfo_check = 0
			},
		},
	}

</script>