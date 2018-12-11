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
		<div v-if="!iser(datas)">
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
					<div role="row" v-for="entry, index in datas" v-if="index>=start&&index<end" class=tr>
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
			<nav v-if="numpage>1" style="text-align:center;  cursor:pointer;">
		        <ul class="pagination">
					<li class="page-item">
						<a class="page-link" tabindex="-1" @click="pagin_change('-1')">上一頁</a>
					</li>
					<!-- <li class="page-item"><a class="page-link">1</a></li> -->

					<li
						:class="{ active: pagenow === 1 }"
						v-if="numpage > 0"
						class="page-item"
					>
						<a class="page-link" tabindex="-1" @click="pagin_change(1)">1</a>
					</li>

					<li v-if="showPrevMore">
						<a class="page-link" tabindex="-1" @click="pagin_change('quickprev')">...</a>
					</li>

					<li
						v-for="pager in pagers"
						:key="pager"
						:class="{ active: pagenow === pager }"
						class="page-item"
					>
						<a class="page-link" tabindex="-1" @click="pagin_change(pager)">{|{ pager }|}</a>
					</li>

					<li v-if="showNextMore">
						<a class="page-link" tabindex="-1" @click="pagin_change('quicknext')">...</a>
					</li>

					<li
						:class="{ active: pagenow === numpage }"
						class="page-item"
						v-if="numpage > 1"
					>
						<a class="page-link" tabindex="-1" @click="pagin_change(numpage)">{|{ numpage }|}</a>
					</li>

					<li class="page-item">
						<a class="page-link" tabindex="-1" @click="pagin_change('+1')">下一頁</a>
					</li>
				</ul>
			</nav>
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
				showPrevMore: false,
				showNextMore: false,
				pagerCount: 7,
			}
		},
		computed: {
			numpage: function () {
				return Math.ceil(this.datas.length / this.numperpage);
			},
			numrow: function () {
				return this.datas.length
			},
			start: function () {
				return this.numperpage *(this.pagenow -1)
			},
			end: function () {
				return Math.min(this.numperpage *(this.pagenow), this.numrow)
			},
			pagers() {
				const pagerCount = this.pagerCount;
				const halfPagerCount = (this.pagerCount - 1) / 2;
				const currentPage = Number(this.pagenow);
				const pageCount = Number(this.numpage);
				let showPrevMore = false;
				let showNextMore = false;
				if (pageCount > pagerCount) {
					if (currentPage > pagerCount - halfPagerCount) {
					  showPrevMore = true;
					}
					if (currentPage < pageCount - halfPagerCount) {
					  showNextMore = true;
					}
				}
				const array = [];
				if (showPrevMore && !showNextMore) {
					const startPage = pageCount - (pagerCount - 2);
					for (let i = startPage; i < pageCount; i++) {
					  array.push(i);
					}
				} 
				else if (!showPrevMore && showNextMore) {
					for (let i = 2; i < pagerCount; i++) {
					  array.push(i);
					}
				} 
				else if (showPrevMore && showNextMore) {
					const offset = Math.floor(pagerCount / 2) - 1;
					for (let i = currentPage - offset; i <= currentPage + offset; i++) {
					  array.push(i);
					}
				} 
				else {
					for (let i = 2; i < pageCount; i++) {
					  array.push(i);
					}
				}

				this.showPrevMore = showPrevMore;
				this.showNextMore = showNextMore;
				return array;
			},
		},
		watch: {
			datas: function (val) {
				this.pagenow = 1
			},
		},
		methods: {
			pagin_change(oper) {
				const pagerCountOffset = this.pagerCount - 2;

				if (String(oper) === '+1') {
					this.pagenow += 1;
				} 
				else if (String(oper) === '-1') {
					this.pagenow -= 1;
				} 
				else if (String(oper) === 'quickprev') {
					this.pagenow = this.pagenow - pagerCountOffset;
				} 
				else if (String(oper) === 'quicknext') {
					this.pagenow = this.pagenow + pagerCountOffset;
				} 
				else {
					this.pagenow = parseInt(oper, 10);
				}

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
				this.datas.sort(compare(this.key, this.orderby))
			},
		},
	}

</script>