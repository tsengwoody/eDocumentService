<template>
	<div style="padding:20px 20px; background-color:#fafafa;">

		<div class="row">
			<div class="col-sm-6">
				<viewer ref="viewer" 
					:pk="pk" 
					:height="400"
					:images="image"
				>
					<li>
						<a href="#" aria-label="文字放大" @click="changeFontSize">
							文字大小 {{ fontSize - 40 }}%
						</a>
					</li>
				</viewer>
			</div>

			<div class="col-sm-6">
				<div id="textSection">
					<div :style="{ fontSize: fontSize + '%', lineHeight: '1.8em' }">
						{{ content }}
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
	module.exports = {
		props: ['pk',],
		components: {
			'viewer': components['viewer'],
		},
		data(){
			return {
				image: {},
				content: '',
				fontSize: 140,
			}
		},
		mounted(){
			if (this.pk) {
				this.refresh();
			}
		},
		methods: {
			instance_set(event){
				this.pk = event;
				this.refresh();
			},
			refresh(){
				//read text data
				let tu = '/ebookSystem/api/ebooks/' + this.pk  + '/resource/OCR/origin';
				Promise.all([
					ebookSystemAPI.ebookRest.read(this.pk),
					axios.get(tu),
				])
				.then(res => {
					this.image = res[0].data.scan_image;
					this.content = _.escape(res[1].data);
				})
			},
			changeFontSize(){
				if (this.fontSize < 200) {
					this.fontSize = this.fontSize + 20;
				} else {
					this.fontSize = 140;
				}
			}
		},
	}

</script>

<style>
div#textSection {
	height:450px; 
	overflow-y:scroll; 
	color:#000; 
	background-color:#fff;
	white-space: pre-wrap;
    word-wrap: break-word;
    word-break: break-all;
}
</style>