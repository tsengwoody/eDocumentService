<template>
	<div id="bookinfo_repository_filter">
		<table-div :datas="datas" :header="header" :tdwidths="tdwidths">
			<template slot="action" slot-scope="props">
				<button class="btn btn-default" @click="check_create(props.item)">借閱</button>
				<a class="btn btn-default" role="button"
					:href="'/ebookSystem/library_origin_view?ISBN=' +props.item"
					target="_blank" title="閱讀(另開新視窗)"
				>閱讀</a>
				<button class="btn btn-default"
					@click="
						feedback_id = props.item;

						$refs[id].open('bookinfo_repository_filter');
					">回報</button>
			</template>
		</table-div>
		<modal :id_modal="id" :size="'normal'" :ref="id">
			<template slot="header">
				<h4 class="modal-title">書籍 {{ feedback_id }} 錯誤內容回報</h4>
			</template>
			<template slot="body">
				<h5>回報內容:</h5>
				<textarea class="feedback" 
					v-model="feedback_content"
				></textarea>
			</template>
			<template slot="footer">
				<button
					class="btn btn-default"
					@click="$refs[id].close()"
				>取消</button>
				<button
					class="btn btn-default"
					@click="feedback()"
				>回報</button>
			</template>
		</modal>
	</div>
</template>

<script>

	module.exports = {
		props: ['header', 'datas',],
		components: {
			'modal': components['modal'],
			'table-div': components['table-div-order'],
		},
		data(){
			return {
				id: Math.floor(Math.random() * 100000000).toString(),
				feedback_id: '',
				feedback_content: '',
				tdwidths: [10, 50, 5, 5, 10, 10, 10]
			}
		},
		methods: {
			check_create(ISBN) {
				ebookSystemAPI.libraryRecordAction.checkCreate({ISBN})
				.then(res => {
					return ebookSystemAPI.libraryRecordAction.checkInout({
						pk: res.data.id,
						action: 'check_out',
					})
				})
				.then(res => {
					alertmessage('success', '成功借閱書籍')
				})
				.catch(res => {
					alertmessage('error', o2j(res.response.data));
				})

			},
			feedback(){
				ebookSystemAPI.bookAction.feedback(this.feedback_id, {
					content: this.feedback_content,
				})
				.then(res => {
					alertmessage('success', '成功回報資料')
				})
				.catch(res => {
					alertmessage('error', o2j(res.response.data));
				})
			},
		},
	}
</script>

<style>
.feedback {
	width: fill-available; 
	width: -webkit-fill-available; 
	height: 200px;
	color:  #4d4d4d;
	font-size: 1.2em;
}
</style>