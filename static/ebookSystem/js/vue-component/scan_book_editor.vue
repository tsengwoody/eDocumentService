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
							文字大小 {|{ fontSize - 40 }|}%
						</a>
					</li>
				</viewer>
			</div>

			<div class="col-sm-6">
				<div id="textSection">
					<div :style="{ fontSize: fontSize + '%', lineHeight: '1.8em' }">
						{|{ content }|}
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
		data: function(){
			return {
				image: {},
				content: '',
				fontSize: 140,
			}
		},
		mounted: function () {
			if (this.pk) {
				this.refresh();
			}
		},
		methods: {
			instance_set: function (event) {
				this.pk = event
				this.refresh();
			},
			refresh: function () {
				//ebooks
				const self = this;
				let client = new $.RestClient('/ebookSystem/api/');
				client.add('ebooks');

				//read text data
				let tu = '/ebookSystem/api/ebooks/' + this.pk  + '/resource/OCR/origin';

				//when
				$.when(client.ebooks.read(this.pk), $.get(tu))
					.done(function(data_pic, data_text){
						self.image = data_pic[0].scan_image;
						self.content =  _.escape(data_text[0]);
					})
			},
			changeFontSize: function() {
				if (this.fontSize < 200) {
					this.fontSize = this.fontSize + 20;
				} else {
					this.fontSize = 140;
				}
			}
		},
		computed: {}
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