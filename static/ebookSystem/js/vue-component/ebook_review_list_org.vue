<template>
	<div class="tab-content" style="padding:20px 0px;">
		<h3>{|{ org.name }|}</h3>
		<div id="ebook_review_list">
			<table-div :header="ebook_header" :datas="ebook_datas">
				<template slot="action" slot-scope="props">
					<a
						role="button" class="btn btn-default"
						:href="'/routing/ebookSystem/ebook_review/' +props.item.ISBN_part +'/'"
						target="blank" title="(另開新視窗)"
					>審核</a>
				</template>
			</table-div>
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
				ebook_header: {
					bookname: '文件',
					part: '段數',
					action: '動作',
				},
				ebook_datas: [],
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
			this.clientb.add('ebooks');
			this.review_list()
		},
		methods: {
			review_list: function () {
				let self = this;
				self.ebook_datas = [];

				self.clientb.ebooks.read({'status': '3', 'org_id': self.org_id,})
				.done(function(data) {
					let filter_data = [];
					_.each(data, function(v){
						filter_data.push({
							bookname: v.bookname,
							part: v.part,
							action: v,
						})
					})
					self.ebook_datas = filter_data;

				})
				.fail(function(xhr, result, statusText){
					alertmessage('error', xhr.responseText)
				})
			},
		},
	}
</script>