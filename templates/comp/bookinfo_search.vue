{% include 'comp/table-div.vue' %}
<template id="bookinfo_search">
<div id="bookinfo_search_div">
	<div v-if="mode==='request'">

		<ul class="nav nav-tabs">
			<li class="active" name="divmodal_FindBook_tab_grp" mode="easy">
				<a @click="source='intergrate'" href="#divmodal_FindBook_tab_easy" data-toggle="tab" aria-expanded="true">綜合查詢</a>
			</li>
			<li name="divmodal_FindBook_tab_grp" mode="adv">
				<a @click="source='ncl'" href="#divmodal_FindBook_tab_adv" data-toggle="tab" aria-expanded="false">國圖查詢</a>
			</li>
		</ul>
		{|{ source }|}
		<div class="tab-content" style="background-color:#fff;">

			<div id="divmodal_FindBook_tab_easy" class="tab-pane active">
				<div style="margin:20px 0px 10px 0px;">輸入書籍ISBN或書名進行查詢：</div>
				<input id="mixvalue" type="text" class="form-control">
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

		<div>
			<button class="btn btn-danger">取消</button>
			<button @click="FindBook()" class="btn btn-primary">取得</button>
			<img id="divmodal_FindBook_loader" src="/static/ebookSystem/img/load.gif" style="display: none;" width="30px" height="30px"/>
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
		<button class="btn btn-danger">取消</button>
		<button class="btn btn-primary" @click="bookinfo_out(bookinfo_check)">確定</button>
	</div>
</div>
</template>
<script>
	Vue.options.delimiters = ['{|{', '}|}'];

	Vue.component('bookinfo_search', {
		template: '#bookinfo_search',
		props: [],
		data: function(){
			return {
				mode: 'request', //request, response
				source: 'intergrate', //intergrate, ncl, douban
				intergrate_value: '',
				default_ncl_query: {
					source: 'NCL',
					'FO_SchRe1ation0': 'Null',
					'FO_SearchField0': 'Title',
					'FO_SearchValue0': '',
					'FO_SchRe1ation1': 'AND',
					'FO_SearchField1': 'ISBN',
					'FO_SearchValue1': '',
					'FO_SchRe1ation2': 'AND',
					'FO_SearchField2': 'Author',
					'FO_SearchValue2': '',
				},
				ncl_query: {
					source: 'NCL',
					'FO_SchRe1ation0': 'Null',
					'FO_SearchField0': 'Title',
					'FO_SearchValue0': '',
					'FO_SchRe1ation1': 'AND',
					'FO_SearchField1': 'ISBN',
					'FO_SearchValue1': '',
					'FO_SchRe1ation2': 'AND',
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
		computed: {
		},
		created: function () {
		},
		mounted: function () {
		},
		methods: {
			FindBook: function () {
				let self = this

				//loading
				self.mode = 'loading'

				//df
				let df;
				let bdone = false;
				if (self.source=== 'intergrate') {
					ncl_query = _.clone(self.default_ncl_query)
					ncl_query['FO_SearchValue0'] = self.intergrate_value
					ncl_query['FO_SearchValue1'] = self.intergrate_value
					df1 = rest_aj_send('post', '/ebookSystem/api/bookinfos/action/key2bookinfo/', ncl_query)
					douban_query = _.clone(self.default_douban_query)
					douban_query['search_query'] = self.intergrate_value
					df2 = rest_aj_send('post', '/ebookSystem/api/bookinfos/action/key2bookinfo/', douban_query)
					df = $.when(df1, df2)
				}
				else if (self.source === 'ncl') {
					df = rest_aj_send('post', '/ebookSystem/api/bookinfos/action/key2bookinfo/', self.ncl_query)
				}

				//done
				df
				.done(function (data) {
					//bdone
					if (bdone === true) {
						return;
					}

					index = 0
					_.each(data['data'].bookinfo_list, function (v) {
						self.result.push({
							"check": index,
							"ISBN": v['ISBN'],
							"bookname": v['bookname'],
							"bookbinding": v['bookbinding'],
							"order": v['order'],
							"author": v['author'],
							"house": v['house'],
							"date": v['date'],
							"chinese_book_category": v['chinese_book_category'],
							"source": "NCL",
						})
						index = index +1
					})

					//切換顯示
					self.mode = 'response'
				})
				.fail(function(xhr, result, statusText){
					//console.log(xhr)
					alertmessage('error', xhr.responseText)
					self.mode = 'request'
				})
				.always(function () {
					bdone = true;
				})

				//等待時間限制
				_.delay(function () {
					if (bdone === false) {

						//bdone
						bdone = true;

						//alert
						alert('等待時間過長，可能是網路問題或符合結果過多，請重新輸入更多書籍資訊。');
						self.mode = 'request'
					}
				}, 1000 * 60);

			},
			bookinfo_out: function (index) {
				let self = this
				self.$emit('bookinfo-out', self.result[index])
			},
		},
	})

</script>