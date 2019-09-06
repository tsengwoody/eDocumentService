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

<template>
	<div>
		<div v-if="!iser(datas)">
			<div role="table" class="table">
				<div role="rowgroup" class=thead>
					<div role="row" class=tr>
						<div v-for="(value, key) in header" role="columnheader" class=cell>
							{{ value }}
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
								{{ entry[key] }}
							</div>
						</template>
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
							<a class="page-link" tabindex="-1" @click="pagin_change(pager)">{{ pager }}</a>
						</li>

						<li v-if="showNextMore">
							<a class="page-link" tabindex="-1" @click="pagin_change('quicknext')">...</a>
						</li>

						<li
							:class="{ active: pagenow === numpage }"
							class="page-item"
							v-if="numpage > 1"
						>
							<a class="page-link" tabindex="-1" @click="pagin_change(numpage)">{{ numpage }}</a>
						</li>

						<li class="page-item">
							<a class="page-link" tabindex="-1" @click="pagin_change('+1')">下一頁</a>
						</li>
					</ul>
				</nav>
			</div>
		</div>
		<div v-else>
			無資料
		</div>
	</div>
</template>

<script>

	module.exports = {
		mixins: [base_table],
	}

</script>