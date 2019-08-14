<template>
	<div class="tab-content">
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
		mounted(){
			genericUserAPI.organizationRest.read(this.org_id)
			.then(res => {
				this.org = res.data
			})
			.catch(res => {
				alertmessage('error', o2j(res.response.data));
			})
			this.review_list()
		},
		methods: {
			review_list(){
				ebookSystemAPI.ebookRest.filter({'status': '3', 'org_id': this.org_id,})
				.then(res => {
					this.ebook_datas = [];
					_.each(res.data, (v)=> {
						this.ebook_datas.push({
							bookname: v.bookname,
							part: v.part,
							action: v,
						})
					})
				})
				.catch(res => {
					alertmessage('error', o2j(res.response.data));
				})
			},
		},
	}
</script>