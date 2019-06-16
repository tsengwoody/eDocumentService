<template>
	<div>
		<h2>文件上傳</h2>
		<book_upload format="epub"></book_upload>
	</div>
</template>

<script>
	module.exports = {
		components: {
			'book_upload': components['book_upload'],
		},
		metaInfo: {
			title: '電子檔上傳',
		},
	}
</script>