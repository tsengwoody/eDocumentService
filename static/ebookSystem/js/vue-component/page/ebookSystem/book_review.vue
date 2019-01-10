
<template>
	<div>
		<h2>文件審核</h2>

		<div id="book_review">
			<h3><span class="glyphicon glyphicon-check" aria-hidden="true" style="margin-top:20px;"></span> Step1: 基本資料</h3>
			<hr style="margin-top:5px;">

			<ul>
				<li
					v-for="(value, key) in info"
				>
					{|{ key }|}:{|{ value }|}
				</li>
			</ul>

			<!-- step 2 -->
			<h3><span class="glyphicon glyphicon-check" aria-hidden="true" style="margin-top:20px;"></span> Step2: 掃描內容</h3>
			<hr style="margin-top:5px;">

			<template  v-for="item in book.ebook_set">
				<button
					style="margin: 0.5em;"
					class="btn btn-default"
					@click="ScanBookEditor('掃描內容瀏覽', item)"
				>分段{|{ item.split('-')[1] }|}</button>
			</template>

			<!--step 3-->
			<h3><span class="glyphicon glyphicon-check" aria-hidden="true" style="margin-top:20px;"></span> Step3: 審核結果</h3>
			<hr style="margin-top:5px;">

			<template v-if="book.status==0">
				<div class="form-group">
					<input type="radio" id="success" value="success" v-model="result">
					<label for="success">成功</label>
					<br>
					<input type="radio" id="error" value="error" v-model="result">
					<label for="error">退回</label>
					<br>
					<template v-if="result=='error'">
						<label for="reason">原因</label>
						<input type="text" id="reason" v-model="reason">
					</template>
				</div>
				<button  class="btn btn-primary" @click="review()" type="submit" id="send_id" name="send">送出</button>
			</template>

		</div>
	</div>
</template>

<script>

	module.exports = {
		data: function() {
			return {
				pk: '',
				book: {},
				info: {},
				reason: '',
				result: 'success', //success or error
			}
		},
		watch: {
			book: function() {
				this.info = {
					'ISBN': this.book.book_info.ISBN,
					'書名': this.book.book_info.bookname,
					'作者': this.book.book_info.author,
					'出版社': this.book.book_info.house,
					'出版日期': this.book.book_info.date,
					'裝訂冊數': this.book.book_info.bookbinding,
				};
			}
		},
		mounted: function () {
			document.title = '文件審核';
			this.pk = window.location.pathname.split('/');
			this.pk = this.pk[this.pk.length-2];
			this.client = new $.RestClient('/ebookSystem/api/');
			this.client.add('books');
			this.get_book_data()
		},
		methods: {
			get_book_data: function(){
				let self = this;

				self.client.books.read(self.pk)
				.done(function(data) {
					self.book = data;
				})
			},
			review: function () {
				let self = this

				const transferData = {
					'result': this.result,
					'reason': this.reason,
				};

				rest_aj_send('post', '/ebookSystem/api/books/' +self.pk +'/action/review/', transferData)
				.done(function(data) {
					alertmessage('success', '審核已完成' + data['data']['message'])
					.done(function() {
						window.location.replace('/routing/ebookSystem/book_review_list/')
					})
				})
				.fail(function(data){
					alertmessage('error', o2j(data))
					.done(function() {
						window.location.replace('/routing/ebookSystem/book_review_list/')
					})
				})
			},
		}
	}
</script>
