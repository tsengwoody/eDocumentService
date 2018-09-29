<template id="businesscontent_instance">
	<div class="row">
		<h2>{|{ name }|}</h2>
	<p v-html="markdown2html(content)"></p>
	</div>
</template>
<script>

	Vue.options.delimiters = ['{|{', '}|}'];

	Vue.component('businesscontent', {
		template: '#businesscontent_instance',
		props: ['pk',],
		data: function(){
			return {
				name: '',
				content: '',
			}
		},
		created: function () {
			let self = this
			self.client = new $.RestClient('/genericUser/api/')
			self.client.add('businesscontents');
		},
		mounted: function () {
			let self = this

			self.client.businesscontents.read(self.pk)
			.done(function(data) {
				self.name = data.name
				self.content = data.content
			})
		},
		methods: {
			markdown2html: function (text) {
				var converter = new showdown.Converter()
				html = converter.makeHtml(text)
				return html
			},
		},
	})

</script>