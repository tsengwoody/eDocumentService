<template>
	<div>
		<ul class="nav nav-tabs">
			<template v-for="(entry, index) in data">
				<template v-if="index===tab_index">
					<li role="tab" class="active"><a :href="'#' +index" aria-expanded="true" @click="tab_index=index">{{ entry.display_name }}</a></li>
				</template>
				<template v-else>
					<li role="tab"><a :href="'#' +index" aria-expanded="false" @click="tab_index=index">{{ entry.display_name }}</a></li>
				</template>
			</template>
		</ul>
		<div class="tab-content" style="padding:20px 0px;">
			<div
				:id="index"
				v-for="(entry, index) in data"
				:class="{'tab-pane':true, 'fade':!(index===tab_index), 'active':(index===tab_index)}"
			>

				<h2 v-if="headinglevel===2" class="sr-only">{{ entry.display_name }}</h2>
				<h3 v-if="headinglevel===3" class="sr-only">{{ entry.display_name }}</h3>
				<h4 v-if="headinglevel===4" class="sr-only">{{ entry.display_name }}</h4>
				<h5 v-if="headinglevel===5" class="sr-only">{{ entry.display_name }}</h5>
				<h6 v-if="headinglevel===6" class="sr-only">{{ entry.display_name }}</h6>

				<div v-if="$scopedSlots[entry.type]">
					<slot :name="entry.type" :item="entry.data"></slot>
				</div>
				<div v-else>
					{{ entry.data }}
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
		data: function() {
			return {
				tab_index: 0,
			}
		},
	}
</script>