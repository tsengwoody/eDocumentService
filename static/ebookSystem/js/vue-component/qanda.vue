<template>
	<div>
		<button
			v-if="user.is_supermanager"
			class="btn btn-primary"
			@click="qanda_create()"
		>新建</button>
		<table-div-row :header="qanda_tutorial_header" :datas="qanda_tutorial_datas">
			<template slot="order" slot-scope="props">
				{{ props.item.order +1 }}
			</template>
			<template slot="question" slot-scope="props">
				<div v-html="props.item"></div>
			</template>
			<template slot="answer" slot-scope="props">
				<div v-html="props.item"></div>
			</template>
			<template slot="action" slot-scope="props">
				<button
					v-if="user.is_supermanager"
					class="btn btn-primary"
					@click="qanda_update(props.item.id)"
				>編輯</button>
				<!--data-toggle="modal" :data-target="'#qm'"-->
				<button
					v-if="user.is_supermanager"
					class="btn btn-primary"
					@click="qanda_del(props.item.id)"
				>刪除</button>
			</template>
		</table-div-row>
		<modal id_modal="qm" ref="qm_instance">
			<template slot="header">
				<h4 class="modal-title">Q&A 編修</h4>
			</template>
			<template slot="body">
				<div class="form-group">
					<label for="id_question" class="control-label"><font style="color:red">*</font>問題</label>
					<editor id="id_question" v-model="qanda_instance.question" :init="tinymce_init"></editor>
					{{ qanda_instance.question }}
				</div>
				
				<hr>
				<div class="form-group">
					<label for="id_answer" class="control-label"><font style="color:red">*</font>回答</label>
					<editor id="id_answer" v-model="qanda_instance.answer" :init="tinymce_init"></editor>
					{{ qanda_instance.answer }}
				</div>
				
			</template>
		</modal>
	</div>
</template>
<script>

	module.exports = {
		props: {
			category: {
				type: String,
			},
		},
		components: {
			'editor': Editor,
			'modal': components['modal'],
			'table-div-row': components['table-div-row'],
		},
		data(){
			return {
				tinymce_init: {
					selector: "editor",
					language:"zh_TW",
					plugins: ['advlist autolink lists link image charmap print preview hr anchor pagebreak', 'searchreplace wordcount visualblocks visualchars code fullscreen', 'insertdatetime media nonbreaking save table contextmenu directionality', 'emoticons template paste textcolor colorpicker textpattern imagetools codesample toc'],
					toolbar: 'undo redo | insert | styleselect | bold italic | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | link image | print preview media | forecolor backcolor emoticons | codesample'
				},
				qanda_tutorial_header: {
					'order': '項次',
					'question': '問題',
					'answer': '回答',
					'action': '動作'
				},
				qanda_tutorial_datas: [],
				qanda_instance: {
					'category': '',
					'question' :'',
					'answer': '',
					'order': '',
				},
			}
		},
		metaInfo: {
			title: '教學文件',
		},
		mounted(){
			this.qanda_list_refresh()
		},
		methods: {
			qanda_list_refresh(){
				this.qanda_tutorial_datas = []
				genericUserAPI.qAndARest.filter({category: this.category,})
				.then(res => {
					let filter_data = []
					_.each(res.data, (v) => {
						let temp_data = {
							'order': v,
							'question': v.question,
							'answer': v.answer,
							"action": v,
						}
						filter_data.push(temp_data)
					})
					this.qanda_tutorial_datas = filter_data
				})
			},
			qanda_create(){
				AboutQAndA('', '', 'tutorial')
				.done((nq, na, nc) => {
					this.qanda_instance.question = nq
					this.qanda_instance.answer = na
					this.qanda_instance.category = nc
					this.qanda_instance.order = 0
					genericUserAPI.qAndARest.create(this.qanda_instance)
					.then(res => {
						alertmessage('success', '成功新建教學內容。')
						this.qanda_list_refresh()
					})
					.catch(res => {
						alertmessage('error', o2j(res.response.data));
					})
				})
			},
			qanda_update(pk){
				genericUserAPI.qAndARest.read(pk)
				.then(res => {
					_.each(this.qanda_instance, (v, k) => {
						this.qanda_instance[k] = res.data[k]
					})
				})
				let qa = this.qanda_instance

				//AboutQAndA
				AboutQAndA(qa.question,qa.answer, qa.category)
				.done((nq, na, nc) => {
					this.qanda_instance.question = nq
					this.qanda_instance.answer = na
					this.qanda_instance.category = nc
					genericUserAPI.qAndARest.update(pk, this.qanda_instance)
					.then(res => {
						alertmessage('success', '成功更新教學內容。')
						this.qanda_list_refresh()
					})
					.catch(res => {
						alertmessage('error', o2j(res.response.data));
					})
				})
			},
			qanda_del(pk){
				alertconfirm('確認刪除 Q&A id:' +pk)
				.done(() => {
					genericUserAPI.qAndARest.delete(pk)
					.then(res => {
						alertmessage('success', '成功刪除 Q&A id:' +pk)
						this.qanda_list_refresh()
					})
					.catch(res => {
						alertmessage('error', o2j(res.response.data));
					})
				})
			},
		},
	}
</script>