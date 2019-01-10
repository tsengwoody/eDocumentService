<template>
	<div>
		<h3>{|{ org.name }|}</h3>
		<div class="tab-content" style="padding:20px 0px;">
			<div id="book_unreview_list">
				<table-div :header="book_header" :datas="book_datas">
					<template slot="action" slot-scope="props">
						<a
							role="button" class="btn btn-default"
							:href="'/routing/ebookSystem/book_review/' +props.item.ISBN +'/'"
							target="blank" title="(另開新視窗)"
						>審核</a>
						<a
							role="button" class="btn btn-default"
							:href="'/routing/ebookSystem/book_detail/' +props.item.ISBN +'/'"
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
		props: ['org_id',],
		components: {
			'table-div': components['table-div'],
		},
		data: function() {
			return {
				org: {},
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
			let self = this

			this.clientg = new $.RestClient('/genericUser/api/');
			this.clientg.add('organizations');
			this.clientg.organizations.read(this.org_id)
			.done(function(data) {
				self.org = data
			})
			.fail(function(xhr, result, statusText){
				alertmessage('error', xhr.responseText)
			})

			this.clientb = new $.RestClient('/ebookSystem/api/');
			this.clientb.add('books');

			self.clientb.books.read({'status': '0', 'org_id': self.org_id})
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