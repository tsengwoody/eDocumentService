<template id="tab">
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
				<h4 class="textfornvda">{|{ entry.display_name }|}</h4>
				<div v-if="$scopedSlots[entry.type]">
					<slot :name="entry.type" :item="entry.data"></slot>
				</div>
				<div v-else>
					{|{ entry.data }|}
				</div>
			</div>
		</div>
	</div>
</template>
<script>
	Vue.options.delimiters = ['{|{', '}|}'];

	Vue.component('tab', {
		template: '#tab',
		props: {
			data: Array,  // define type
		},
	})
</script>