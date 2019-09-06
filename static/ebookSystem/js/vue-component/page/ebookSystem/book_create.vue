<template>
	<div>
		<h2>文件上傳</h2>
		<book_upload format="self"></book_upload>
	</div>
</template>

<script>
	module.exports = {
		components: {
			'book_upload': components['book_upload'],
		},
		metaInfo: {
			title: '掃描檔上傳',
		},
		mounted(){
			//document.title = '掃描檔上傳';
		},
	}
</script>
