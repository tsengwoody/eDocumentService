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
		data(){
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
		mounted(){
			if(!(this.org_id==='all')){
				this.refresh_org()
			} else {
				this.org = {
					'name': '全部',
				}
			}
			this.statistics()
		},
		watch: {
			org_id(){
				if(!(this.org_id==='all')){
					this.refresh_org()
				} else {
					this.org = {
						'name': '全部',
					}
				}
				this.statistics()
			},
		},
		methods: {
			refresh_org(){
				genericUserAPI.organizationRest.read(this.org_id)
				.then(res => {
					this.org = res.data
				})
				.catch(res => {
					alertmessage('error', o2j(res.response.data));
				})
			},
			statistics(){
				let pageURL = new URL(window.location.href)
				let page_params = {}
				for (let pair of pageURL.searchParams.entries()) {
					page_params[pair[0]] = pair[1]
				}

				let querys = []
				let keys = []
				let params = {}
				params = Object.assign(params, page_params)

				if(!(this.org_id==='all')){
					params = Object.assign(params, {'org_id': this.org_id})
				}

				let all_query = axios.get(this.url, params)
				querys.push(all_query)

				all_query
				.then(res => {
					let key = 'all'
					this['temp'][key] = []
					_.each(res.data.result, (item) => {
						temp_obj = {}
						temp_obj['groupfield'] = item.groupfield
						temp_obj[key] = item.count
						this['temp'][key].push(temp_obj)
					})
				})
				.catch(res => {
					alertmessage('error', o2j(res.response.data));
				})

				_.each([0, 1, 2, 3, 4, 5, 6,], (v) => {
					let time = genMonth(v)
					let begin_time = time['begin_time']
					let end_time = time['end_time']

					let key = 'month' +v
					let month_query = axios.get(this.url, {params: {
						...params,
						...{begin_time, end_time,},
					}})
					querys.push(month_query)
					keys.push(key)
						this.statistics_header[key] = begin_time.split('-')[0] +'年' +begin_time.split('-')[1] +'月'

					month_query
					.then(res => {
						let k = key
						this['temp'][k] = []
						_.each(res.data.result, (item) => {
							temp_obj = {}
							temp_obj['groupfield'] = item.groupfield
							temp_obj[k] = item.count
							this['temp'][k].push(temp_obj)
						})
					})
					.catch(res => {
						alertmessage('error', o2j(res.response.data));
					})
				})

				Promise.all(querys)
				.then(() => {
					this.statistics_datas = this.temp['all']
					_.each(keys, (v) => {
						this.statistics_datas = $.extendObjectArray(this.statistics_datas, this.temp[v], 'groupfield')
					})
					fill_cell(this.statistics_datas, Object.keys(this.statistics_header), '0')
				})
				.catch(res => {
					alertmessage('error', o2j(res.response.data));
				})
			},
		},
	}
</script>