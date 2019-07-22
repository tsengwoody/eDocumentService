<template>
	<div>
		<h3>{|{ org.name }|}</h3>
		<div class="tab-content">
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
		data(){
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
		mounted(){
			genericUserAPI.organizationRest.read(this.org_id)
			.then(res => {
				this.org = res.data
			})
			.catch(res => {
				alertmessage('error', o2j(res.response.data));
			})

			ebookSystemAPI.bookRest.filter({'status': '0', 'org_id': self.org_id})
			.then(res => {
				this.book_datas = [];
				_.each(res.data, (v) => {
					this.book_datas.push({
						'ISBN': v.ISBN,
						'bookname': v.book_info.bookname,
						'page': v.finish_page_count +'/' +v.page_count,
						'finish_part_count': v.finish_part_count,
						'service_hours': v.service_hours,
						'action': v,
					})
				})
			})
			.catch(res => {
				alertmessage('error', o2j(res.response.data));
			})
		},
	}
</script>