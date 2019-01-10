<template>
	<div>
		<h2>文件上傳</h2>
		<book_upload category="epub"></book_upload>
	</div>
</template>

<script>
	module.exports = {
		components: {
			'book_upload': components['book_upload'],
		},
		data: function() {
			return{}
		},
		mounted: function() {
			document.title = '電子檔上傳';
		}
	}
</script>