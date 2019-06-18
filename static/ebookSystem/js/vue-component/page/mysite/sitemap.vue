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
		data(){
			return {
				'items': [],
			}
		},
		mounted(){
			document.title = '網站導覽'

			mode = localStorage.getItem('nav_mode');

			if(!mode) {
				this.mode = 'all'
			}
			else {
				this.mode = mode
			}

			setTimeout(() => {
				let enc;
				if(mode==='all'){
					enc = this.$root.edsnavall
				}
				if(mode==='self'){
					enc = this.$root.edsnavself
				}

				this.items.push(...enc.item_show(enc.nav_item))
				this.items.push(...enc.item_show(enc.nav_item_right))
			}, 100)
		},
	}
</script>
<style >
#sitemap>ul {
	line-height: 1.6em;
}
</style>