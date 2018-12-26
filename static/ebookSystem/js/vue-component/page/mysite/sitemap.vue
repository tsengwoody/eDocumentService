<template>
	<div id="sitemap">
		<h2>網站導覽 <span id="span_more" class="label label-warning" style="display:none; font-size:12pt;">登入後有更多使用者功能!</span></h2>
		<ul>
			<template v-for="item, index in items">
				<template v-if="item.type=='folder'">
					<li><a href="#">{|{ index+1 }|}. {|{ item.display_name }|}</a>
						<ul>
							<template v-for="folder_item, index_in in item.items">
								<li><a :href="folder_item.url">{|{ index+1 }|}.{|{ index_in+1 }|} {|{ folder_item.display_name }|}</a></li>
							</template>
						</ul>
					</li>
				</template>
				<template v-if="item.type=='item'">
					<li><a :href="item.url">{|{ index+1 }|}. {|{ item.display_name }|}</a></li>
				</template>
			</template>
		</ul>
	</div>
</template>
<script>
	module.exports = {
		components: {
			'eds-nav': components['eds-nav'],
		},
		data: function(){
			return {
				'items': [],
			}
		},
		mounted: function () {
			document.title = '網站導覽'
			setTimeout(() => {
				let enc = vo_eds_nav.$refs.eds_nav_instance
				this.items.push(...enc.item_show(enc.nav_item))
				this.items.push(...enc.item_show(enc.nav_item_right))
			}, 1000)
		},
		methods: {
			test: function(){
				c = vo_eds_nav.$refs.eds_nav_instance.nav_item
				console.log(c)
			},
		},
	}
</script>
<style >
#sitemap>ul {
	line-height: 1.6em;
}
</style>