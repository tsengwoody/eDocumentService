<template>
	<div>
		<h2>上傳文件審核</h2>
		<div class="tab-content" style="padding:20px 0px;">
			<div id="book_unreview_list">
				<table-div :header="book_header" :datas="book_datas">
					<template slot="action" slot-scope="props">
						<a
							role="button" class="btn btn-default"
							:href="'/ebookSystem/generics/book_review/' +props.item.ISBN +'/'"
							target="blank" title="(另開新視窗)"
						>審核</a>
						<a
							role="button" class="btn btn-default"
							:href="'/ebookSystem/generics/book_detail/' +props.item.ISBN +'/'"
							target="blank" title="(另開新視窗)"
						>分段資訊</a>
					</template>
				</table-div>
			</div>
		</div>
	</div>
</template>

<script>

	module.exports = {
		components: {
			'table-div': components['table-div'],
		},
		data: function() {
			return {
				book_header: {
					'ISBN': 'ISBN',
					'bookname': '書名',
					'page': '頁數/總頁數',
					'finish_part_count': '已完成段數',
					'service_hours': '時數',
					'action': '動作',
				},
				book_datas: [],
			}
		},
		mounted: function () {
			document.title = '上傳文件審核';
			this.client = new $.RestClient('/ebookSystem/api/');
			this.client.add('books');
			this.client.add('bookadds');

			let self = this
			self.client.books.read({'status': '0',})
			.done(function(data) {
				let filter_data = [];
				_.each(data, function(v){
					filter_data.push({
						'ISBN': v.ISBN,
						'bookname': v.book_info.bookname,
						'page': v.finish_page_count +'/' +v.page_count,
						'finish_part_count': v.finish_part_count,
						'service_hours': v.service_hours,
						'action': v,
					})
				})
				self.book_datas = filter_data
			})
			.fail(function(xhr, result, statusText){
				alertmessage('error', xhr.responseText)
			})
		},
	}
</script>