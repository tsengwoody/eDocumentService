<template>
	<div id="bookorder_list">
		<h2>校對順序</h2>
		<table-div :header="bookorder_header" :datas="bookorder_datas">
		</table-div>
	</div>
</template>

<script>
	module.exports = {
		components: {
			'table-div': components['table-div'],
		},
		data(){
			return {
				bookorder_header: {
					order: '順序',
					bookname: '書名',
					status: '狀態',
				},
				bookorder_datas: [],
			}
		},
		metaInfo: {
			title: '校對順序',
		},
		mounted: function () {
			ebookSystemAPI.bookOrderRest.list()
			.then(res => {
				let filter_data = [];
				_.each(res.data, (v) => {
					filter_data.push({
						order: v.order,
						bookname: v.bookname,
						status: v.status,
					})
				})
				this.bookorder_datas = filter_data;
			})
			.catch(res => {
				alertmessage('error', o2j(res.response.data));
			})

		},
	}
</script>