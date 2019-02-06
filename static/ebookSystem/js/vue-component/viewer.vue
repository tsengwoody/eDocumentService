<template>
	<div :style="{ height: height + 'px', overflow: 'hidden'}">
		<div id="scanPage">
			<img :src="image_url" alt="文件掃描原檔" name="scanPage" style="opacity:0;">
		</div>
	</div>
</template>

<script>
	module.exports = {
		props: {
			height: {
				default: 425,
				type: Number,
			},
			image_url: String,
		},
		data: function() {
			return {
				viewerId: null,
			}
		},
		mounted: function() {
			if (this.image_url) {
				this.refreshViewer();
			}
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
			}
		},
		watch: {
			image_url: function() {
				this.$nextTick(() => {
					this.refreshViewer();
				})
			},
		},
	}
</script>

<style>

li.viewer-prev, li.viewer-play, li.viewer-next, li.viewer-flip-horizontal, 
li.viewer-flip-vertical {
	display: none;
}

</style>