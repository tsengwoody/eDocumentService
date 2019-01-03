<template>
	<div>
		<ul class="nav nav-tabs">
			<template v-for="(entry, index) in data">
				<li role="tab" :class="{'active':(index===0)}"><a :href="'#index_tab_' +entry.value" name="index_tab_grp" data-toggle="tab" :aria-expanded="!!(index===0)" @click="pagetab_subtabfix(this);">{|{ entry.display_name }|}</a></li>
			</template>
		</ul>
		<div class="tab-content" style="padding:20px 0px;">
			<div
				v-for="(entry, index) in data"
				:id="'index_tab_' +entry.value"
				:class="{'tab-pane':true, 'active':(index===0)}"
			>

				<h2 v-if="headinglevel===2" class="sr-only">{|{ entry.display_name }|}</h2>
				<h3 v-if="headinglevel===3" class="sr-only">{|{ entry.display_name }|}</h3>
				<h4 v-if="headinglevel===4" class="sr-only">{|{ entry.display_name }|}</h4>
				<h5 v-if="headinglevel===5" class="sr-only">{|{ entry.display_name }|}</h5>
				<h6 v-if="headinglevel===6" class="sr-only">{|{ entry.display_name }|}</h6>

				<div v-if="$scopedSlots[entry.type]">
					<slot :name="entry.type" :item="entry.data"></slot>
				</div>
				<div v-else>
					{|{ entry.data }|}
				</div>
			</div>
		</div>
	</div>`
</template>

<script>
	module.exports = {
		props: {
			data: Array,  // define type
			headinglevel: Number,
		},
	}
</script>