<template>
	<div>
		<h2>{|{ title }|}</h2>
		<table-div
			:header="statistics_header"
			:datas="statistics_datas"
		></table-div>
	</div>
</template>
<script>
	module.exports = {
		components: {
			'table-div': components['table-div-order'],
		},
		data: function(){
			return {
				statistics_header: {
					'groupfield': '項目',
					'all': '全部期間',
				},
				statistics_datas: [],
				temp: {},
				title: '',
				url: '',
			}
		},
		mounted: function () {
			let self = this
			let page = window.location.pathname.split('/')
			page = page[page.length-2]
			if(page==='book_download'){
				self.title = '統計書籍下載'
			}
			else if(page==='user_download'){
				self.title = '統計使用者下載'
			}
			else if(page==='user_editrecord'){
				self.title = '統計使用者校對'
			}

			document.title = self.title
			self.url = '/api/statistics/' +page +'/'
			this.statistics()
		},
		methods: {
			statistics: function () {
				let self = this;

				let querys = []
				let keys = []

				let all_query = rest_aj_send_memory('get', self.url, {}, {'key': 'all'})
				querys.push(all_query)

				all_query
				.done(function(data) {
					key = data['memory']['key']
					self['temp'][key] = []
					_.each(data['data'].result, function(item){
						temp_obj = {}
						temp_obj['groupfield'] = item.groupfield
						temp_obj[key] = item.count
						self['temp'][key].push(temp_obj)
					})
				})
				.fail(function(xhr, result, statusText){
					console.log(xhr)
				})

				_.each([0, 1, 2, 3, 4, 5, 6,], function(v){

					time = genMonth(v)
					begin_time = time['begin_time']
					end_time = time['end_time']

					key = 'month' +v
					let month_query = rest_aj_send_memory('get', self.url, {'begin_time': begin_time, 'end_time': end_time,}, {'key': key})
					querys.push(month_query)
					keys.push(key)
						self.statistics_header[key] = begin_time.split('-')[0] +'年' +begin_time.split('-')[1] +'月'

					month_query
					.done(function(data) {
						key = data['memory']['key']
						self['temp'][key] = []
						_.each(data['data'].result, function(item){
							temp_obj = {}
							temp_obj['groupfield'] = item.groupfield
							temp_obj[key] = item.count
							self['temp'][key].push(temp_obj)
						})
					})
					.fail(function(xhr, result, statusText){
						console.log(xhr)
					})

				})

				Promise.all(querys)
				.then(function () {
					self.statistics_datas = self.temp['all']
					_.each(keys, function(v){
						self.statistics_datas = $.extendObjectArray(self.statistics_datas, self.temp[v], 'groupfield')
					})
					fill_cell(self.statistics_datas, Object.keys(self.statistics_header), '0')
				})
				.catch(function (msg) {
					console.log(msg)
				})
			},
		},
	}
</script>