<template>
	<div>
		<nav>
			<ul class="pager" style="margin:0px 0px 10px 0px;">
				<li>
					<a href="#" aria-label="至最初頁" @click="changePage('first')">最初頁</a>
				</li>

				<li>
					<a href="#" aria-label="上一頁" @click="changePage(-1)">上一頁</a>
				</li>
				
				<li>
					<div style="display:inline-block; float:none;">
						<select class="form-control" id="scanPageList" 
							v-model="nowPage" 
							@change="$emit('changed', $event.target.value);"
						>
							<template v-for="(value, key) in images">
								<option 
									v-if="edited_page == key"
									:value="key"
								>
									{|{ value }|}-上次校對頁數
								</option>
								<option 
									v-else
									:value="key"
								>
									{|{ value }|}
								</option>
							</template>

						</select>
					</div>
				</li>

				<li>
					<a href="#" aria-label="下一頁" @click="changePage(1)">下一頁</a>
				</li>

				<li>
					<a href="#" aria-label="至最後頁" @click="changePage('end')">最後頁</a>
				</li>

				<slot></slot>
			</ul>
		</nav>

		<div :style="{ height: (newHeight || height) + 'px'}">
			<div id="scanPage">
				<img :src="image_url" alt="文件掃描原檔" name="scanPage" style="opacity:0; height: 0px;">
			</div>
		</div>
	</div>
</template>

<script>
	module.exports = {
		props: {
			pk: String,
			images: Object,
			edited_page: {
				default: null,
				type: Number,
			},
			height: Number,
		},
		data: function() {
			return {
				viewerId: null,
				nowPage: null,
				newHeight: null,
			}
		},
		created: function() {
			this.$parent.$on('updateHeight', this.setHeight);
		},
		mounted: function() {
			this.nowPage = this.edited_page || 0;
			this.$nextTick(() => {
				this.refreshViewer();
			})
		},
		computed: {
			image_url: function() {
				return '/ebookSystem/api/ebooks/' +this.pk +'/resource/source/' +this.nowPage +'/'
			},
		},
		methods: {
			refreshViewer: function() {
				// Destroy the viewer and remove the instance.
				this.viewerId && this.viewerId.destroy();
				this.viewerId = new Viewer(document.getElementById('scanPage'), {
					inline: true,
					button: false,
					navbar: false,
					title: false,
					toolbar: true,
					tooltip: true,
					movable: true,
					zoomable: true,
					rotatable: true,
					scalable: false,
					transition: true,
					fullscreen: false,
					keyboard: false,
					viewed() {
						let imgview_ratio = 
							localStorage.getItem("imgview_ratio") || 0.3;
						this.viewer.zoomTo(imgview_ratio - 0);
					},
					zoomed(event) {
						const ratio = event.detail.ratio;
						localStorage.setItem("imgview_ratio", ratio);
					}
				});
			},
			changePage: function(value) {
				if (value === 'first') this.nowPage = 0;
				else if (value === 'end') this.nowPage = 49;
				else {
					const page = parseInt(this.nowPage) + value;
					if (page >= 0 && page < 50) {
						this.nowPage = page;
					}
					else {
						alertmessage('error', '超過頁數範圍惹~');
					}
				}
			},
			setHeight: function() {
				this.refreshViewer();
			},
		},
		watch: {
			image_url: function() {
				this.$nextTick(() => {
					this.refreshViewer();
				})
			},
			edited_page: function(val) {
				this.nowPage = val;
			},
		},
	}
</script>

<style>

li.viewer-prev, li.viewer-play, li.viewer-next, li.viewer-flip-horizontal, 
li.viewer-flip-vertical {
	display: none;
}

div.viewer-container {
	// resize: vertical;
 	// overflow-y: scroll;
    margin-bottom: 100px;
}

</style>