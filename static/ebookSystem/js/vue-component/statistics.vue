<template>
	<div>
		<h3>{|{ org.name }|}資料</h3>
		<table-div
			:header="statistics_header"
			:datas="statistics_datas"
		></table-div>
	</div>
</template>
<script>
	module.exports = {
		props: ['org_id', 'url', ],
		components: {
			'table-div': components['table-div-order'],
		},
		data: function(){
			return {
				org: {},
				statistics_header: {
					'groupfield': '項目',
					'all': '全部期間',
				},
				statistics_datas: [],
				temp: {},
			}
		},
		created: function () {
			this.clientg = new $.RestClient('/genericUser/api/');
			this.clientg.add('organizations');
		},
		mounted: function () {
				let self = this
			if(!(self.org_id==='all')){
				this.refresh_org()
			} else {
				self.org = {
					'name': '全部',
				}
			}
			this.statistics()
		},
		watch: {
			org_id: function() {
				let self = this
				if(!(self.org_id==='all')){
					this.refresh_org()
				} else {
					self.org = {
						'name': '全部',
					}
				}
				this.statistics()
			},
		},
		methods: {
			refresh_org: function () {
				let self = this
				this.clientg.organizations.read(this.org_id)
				.done(function(data) {
					self.org = data
				})
				.fail(function(xhr, result, statusText){
					alertmessage('error', xhr.responseText)
				})
			},
			statistics: function () {
				let self = this;

				let pageURL = new URL(window.location.href)
				let page_params = {}
				for (let pair of pageURL.searchParams.entries()) {
					page_params[pair[0]] = pair[1]
				}

				let querys = []
				let keys = []
				let params = {}
				params = Object.assign(params, page_params)

				let all_query

				if(!(self.org_id==='all')){
					params = Object.assign(params, {'org_id': self.org_id})
				}

				all_query = rest_aj_send('get', self.url, params)

				querys.push(all_query)

				all_query
				.done(function(data) {
					let key = 'all'
					self['temp'][key] = []
					_.each(data['data'].result, function(item){
						temp_obj = {}
						temp_obj['groupfield'] = item.groupfield
						temp_obj[key] = item.count
						self['temp'][key].push(temp_obj)
					})
				})
				.fail(function(xhr, result, statusText){
					console.log(self.url)
					alertmessage('error', o2j(xhr))
				})

				_.each([0, 1, 2, 3, 4, 5, 6,], function(v){

					let time = genMonth(v)
					let begin_time = time['begin_time']
					let end_time = time['end_time']

					let key = 'month' +v
					params = Object.assign(params, {'begin_time': begin_time, 'end_time': end_time})
					let month_query = rest_aj_send('get', self.url, params)
					querys.push(month_query)
					keys.push(key)
						self.statistics_header[key] = begin_time.split('-')[0] +'年' +begin_time.split('-')[1] +'月'

					month_query
					.done(function(data) {
						let k = key
						self['temp'][k] = []
						_.each(data['data'].result, function(item){
							temp_obj = {}
							temp_obj['groupfield'] = item.groupfield
							temp_obj[k] = item.count
							self['temp'][k].push(temp_obj)
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