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
		data: function() {
			return {
				bookorder_header: {
					order: '順序',
					bookname: '書名',
					status: '狀態',
				},
				bookorder_datas: [],
			}
		},
		mounted: function () {
			document.title = '校對順序';

			this.client = new $.RestClient('/ebookSystem/api/');
			this.client.add('bookorders');

			let self = this
			self.client.bookorders.read()
			.done(function(data) {
				let filter_data = [];
				_.each(data, function(v){
					filter_data.push({
						order: v.order,
						bookname: v.bookname,
						status: v.status,
					})
				})
				self.bookorder_datas = filter_data;
			})
			.fail(function(xhr, result, statusText){
				alertmessage('error', xhr.responseText)
			})
		},
	}
</script>