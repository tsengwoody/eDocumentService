<!--  scoped CSS -->
<style scoped>
div.table {
	width: 100%;
    max-width: 100%;
	display: block;
	border-collapse: collapse;
	border-spacing: 0px;
	margin: 1em auto;
	border-color: grey;
}

div.table .tr {
    display: block;
	border: #ddd 1px solid;
	margin-bottom: 10px;
	text-align: left;
}

div.table > .thead{
	display: none;
}

div.table > .tbody{
	display: block;
}

.tr .cell {
	display: inline-block;
	width: 100%;
	border: none;
	padding: 5px;
}

.tr .cell {
	border-top: 1px solid rgb(221, 221, 221);
	vertical-align: top;
    line-height: 1.42857;
    padding: 8px;
}

.tr .cell::before{
	content: attr(data-title);
	display: block;
	width: auto;
	margin-bottom: 0.5em;
/*		min-width: 40%;*/
	font-weight: 900;
	font-size: 1.2em;
}

</style>

<script type="text/x-template" id="table-template">
	<div>
		<div v-if="!iser(datas)">
			<div role="table" class="table">
				<div role="rowgroup" class=thead>
					<div role="row" class=tr>
						<div v-for="(value, key) in header" role="columnheader" class=cell>
							{|{ value }|}
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
				<div style="text-align:center;">
					<ul class="pagination" style="margin:0px;">
						<li class="prev" style="cursor:pointer;"><a href="#" @click="pagin_change(-1)">上一頁</a></li>
						<li class=""><a>{|{ pagenow }|} / {|{ numpage }|}</a></li>
						<li class="next" style="cursor:pointer;"><a href="#" @click="pagin_change(1)">下一頁</a></li>
					</ul>
				</div>
			</div>
		</div>
		<div v-else>
			無資料
		</div>
	</div>
</script>

<script>
	Vue.options.delimiters = ['{|{', '}|}'];

	Vue.component('table-div-row', {
		props: {
			datas: Array,  // define type
			header: Object,
		},
		data: function () {
			return {
				numperpage: 10,
				pagenow: 1,
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
		},
		watch: {
			datas: function (val) {
				this.pagenow = 1
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
		},
		template: '#table-template',
	})

</script>