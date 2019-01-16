<template>
	<div class="row">
		<div class="col-sm-3 col-md-3">
			<div class="panel-group">
				<div class="panel panel-default">
					<div class="panel-heading">
						<h4 class="panel-title">
							<span class="glyphicon glyphicon-folder-close"></span>&nbsp;&nbsp; {|{ title }|}
						</h4>
					</div>
					<div class="panel-collapse">
						<ul class="list-group">
							<template v-for="(entry, index) in data">
								<li v-if="index===tab_index" class="list-group-item">
									<a href='#' aria-expanded="true" @click="tab_index=index" >{|{ index+1 }|}. {|{ entry.display_name }|}</a>
								</li>
								<li v-else class="list-group-item">
									<a href='#' aria-expanded="false" @click="tab_index=index">{|{ index+1 }|}. {|{ entry.display_name }|}</a>
								</li>
							</template>
						</ul>
					</div>
				</div>
			</div>
		</div>
		<div class="col-sm-9 col-md-9">
			<div v-for="(entry, index) in data">
				<template v-if="tab_index == index">
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
				</template>
			</div>
		</div>
	</div>
</template>

<script>
	module.exports = {
		props: {
			title: String,
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