<template>
	<div>
		<h2>書籍閱讀統計</h2>
			<statistics-book-read
				:org="org"
			></statistics-book-read>
		</template>
	</div>
</template>

<script>
	module.exports = {
		components: {
			panelGroup: components['panel_group'],
			statisticsBookRead: components['statistics_book_read'],
		},
		data(){
			return {
				org: {},
			}
		},
		metaInfo: {
			title: '書籍閱讀統計',
		},
		mounted(){
			this.tab_data = []
			genericUserAPI.organizationRest.read(user.org)
			.then(res => {
				this.org = res.data;
			})
			.catch(res => {
				alertmessage('error', o2j(res.response.data));
			})
		},
	}
</script>

<style>

</style>