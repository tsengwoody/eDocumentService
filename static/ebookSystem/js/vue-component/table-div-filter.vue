<!--  scoped CSS -->
<style scoped>
div.table {
	width: 100%;
    max-width: 100%;
	display: table;
	border-collapse: collapse;
	border-spacing: 0px;
	margin: 10px 0px;
	border-color: grey;
}

div.table .tbody .tr:hover {
	background-color: #f7f7f7;
}

div.table .thead{
	background-color: #eee;
	display: table-header-group;
}

div.table .tr {
	display: table-row;
    border: 0px;
    border-bottom: 1px solid #ddd;
    text-align: center;
}

div.table .tbody{
	display: table-row-group;
}

.thead .cell, .tr .cell{
	display: table-cell;
	padding: 5px;
	border-top: 0px;
}

.thead .cell{
	font-weight: bold;
	line-height: 1.42857;
    vertical-align: top;
    padding: 10px 0px;
}

div.tbody .cell {
	border-top: 1px solid rgb(221, 221, 221);
	vertical-align: top;
    line-height: 1.42857;
    padding: 8px;
}

@media only screen and (max-width:760px) {
	div.table {
		display: block;
		margin: 1em auto;
	}

	div.table .thead{
		display: none;
	}

	div.table .tbody{
		display: block;
	}

	div.table .tr{
		display: block;
		border: #ddd 1px solid;
		margin-bottom: 10px;
		text-align: left;
	}
	.tr .cell{
		display: inline-block;
		width: 100%;
		border: none;
	}
	.tr .cell::before{
		content: attr(data-title);
		display: block;
		width: auto;
/*		min-width: 40%;*/
		font-weight: 900;
		font-size: 1.2em;
	}
}
</style>

<template>
	<div>
		<div style="text-align:center;">
			<form class="form-inline">
				<div class="form-group">
					<input class="form-control" type="text" v-model="keyword">
				</div>
				<div class="form-group">
					<select class="form-control" v-model="selectHeader">
						<option v-for="(v, k) in header" :value="k">{|{ v }|}</option>
					</select>	
				</div>
				<button class="btn btn-primary" @click.prevent="filterData">搜尋</button>
			</form>
		</div>
		<div v-if="!iser(showData)">
			<div role="table" class="table">
				<div role="rowgroup" class=thead>
					<div role="row" class=tr>
						<div v-for="(v, k) in header" role="columnheader" class=cell>
							<a role="button"
								@click="order(k)"
							>
								{|{ v }|}
								<template v-if="k===key">
									<template v-if="orderby==='asc'">▲</template>
									<template v-if="orderby==='desc'">▼</template>
								</template>
							</a>
						</div>
					</div>
				</div>
				<div role="rowgroup" class=tbody>
					<div role="row" v-for="entry, index in showData" v-if="index>=start&&index<end" class=tr>
						<template v-for="(value, key) in header" >
							<div v-if="$scopedSlots[key]" :data-title="value" role="cell" class=cell>
								<slot :name="key" :item="entry[key]"></slot>
							</div>
							<div v-else :data-title="value" role="cell" class=cell>
								{|{ entry[key] }|}
							</div>
						</template>
					</div>
				</div>
			</div>
			<div v-if="numpage>1" style="text-align:center;">
				<ul class="pagination" style="margin:0px;">
					<li class="prev" style="cursor:pointer;"><a href="#" @click="pagin_change(-1)">上一頁</a></li>
					<li class=""><a>{|{ pagenow }|} / {|{ numpage }|}</a></li>
					<li class="next" style="cursor:pointer;"><a href="#" @click="pagin_change(1)">下一頁</a></li>
				</ul>
			</div>
		</div>
		<div v-else>
			無資料
		</div>
	</div>
</template>

<script>

	module.exports = {
		props: {
			datas: Array,  // define type
			header: Object,
		},
		data: function () {
			return {
				key: '',
				orderby: '',
				numperpage: 10,
				pagenow: 1,
				keyword: '',
				selectHeader: '',
				showData: []
			}
		},
		computed: {
			numpage: function () {
				return Math.ceil(this.showData.length / this.numperpage);
			},
			numrow: function () {
				return this.showData.length
			},
			start: function () {
				return this.numperpage *(this.pagenow -1)
			},
			end: function () {
				return Math.min(this.numperpage *(this.pagenow), this.numrow)
			},
		},
		watch: {
			showData: function (val) {
				this.pagenow = 1
			},
			datas: function (val) {
				// initial showData from async datas
				this.showData = val;
			},
		},
		methods: {
			pagin_change: function(oper) {
				//表格分頁切換

				let pagenow = this.pagenow
				let numperpage = this.numperpage
				let numpage = this.numpage

				if (String(oper) === '1') {
					this.pagenow += 1;
				}
				else if (String(oper) === '-1') {
					this.pagenow -= 1;
				}
				else {
					this.pagenow = cint(oper);
				}

				//check
				this.pagenow = Math.max(this.pagenow, 1);
				this.pagenow = Math.min(this.pagenow, this.numpage);
			},
			order: function(key, orderby) {
				if(this.key === key){
					if(this.orderby==='asc'){
						this.orderby = 'desc'
					}
					else if(this.orderby==='desc'){
						this.orderby = 'asc'
					}
					else {
						this.orderby = 'desc'
					}
				}
				else {
					this.orderby = 'desc'
				}
				this.key = key
				this.showData.sort(compare(this.key, this.orderby))
			},
			filterData: function() {
				var self = this;
				self.showData = _.cloneDeep(this.datas)	// re-initialize data before filter

				if(this.keyword && this.selectHeader) {
					var filterByKeyword = this.datas.filter(function(item) {
						if(item[self.selectHeader]) {
							return item[self.selectHeader].indexOf(self.keyword) > -1;
						}
					})
					self.showData = filterByKeyword;
					alertmessage('success', '成功完成搜尋!')
				} else if(!this.selectHeader) {
					alertmessage('error', '請填妥搜尋欄位')
				}
			}
		},
	}

</script>