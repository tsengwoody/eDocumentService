<!-- {% include 'comp/upload_dialog.html' %} -->

<template>
	<div id="book_create">
		<h2>文件上傳</h2>
		<book_upload category="self"></book_upload>
	</div>
</template>

<script>
	module.exports = {
		components: {
			'book_upload': components['book_upload'],
		},
		data: function() {},
		mounted: function() {
			document.title = '掃描檔上傳';
		},
	}
</script>
