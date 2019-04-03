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

				let querys = []
				let keys = []

				let all_query

				if(!(self.org_id==='all')){
					all_query = rest_aj_send_memory('get', self.url, {'org_id': self.org_id}, {'key': 'all'})
				} else {
					all_query = rest_aj_send_memory('get', self.url, {}, {'key': 'all'})
				}

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

					let month_query
					if(!(self.org_id==='all')){
						month_query = rest_aj_send_memory('get', self.url, {'begin_time': begin_time, 'end_time': end_time, 'org_id': self.org_id}, {'key': key})
					} else {
						month_query = rest_aj_send_memory('get', self.url, {'begin_time': begin_time, 'end_time': end_time}, {'key': key})
					}

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