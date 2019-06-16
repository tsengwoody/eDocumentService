<template>
	<div id="user_email">
		<h2>訊息傳送</h2>
		<div class="form-horizontal">
			<form-drf
				:keys="'category'"
				:model_info="model_info.category"
				:label-class="'col-sm-1'"
				:input-class="'col-sm-11'"
				mode="write"
				v-model="category"
			></form-drf>
			<form-drf
				:keys="'subject'"
				:model_info="model_info.subject"
				:label-class="'col-sm-1'"
				:input-class="'col-sm-11'"
				mode="write"
				v-model="subject"
			></form-drf>
			<form-drf
				:keys="'body'"
				:model_info="model_info.body"
				:label-class="'col-sm-1'"
				:input-class="'col-sm-11'"
				mode="write"
				v-model="body"
			></form-drf>
			<div class="form-group">
				<div class="col-sm-offset-1 col-sm-11">
					<button class="btn btn-primary" @click="send_email()">傳送</button>
				</div>	
			</div>
		</div>
	</div>
</template>

<script>
	module.exports = {
		components: {
			'form-drf': components['form'],
		},
		data(){
			return {
				category: 'editor',
				subject: '',
				body: '',
				model_info: {
					'category': {
						'label': '類型',
						'type': 'radio',
						'choices' : [
							{
								'value': 'editor',
								'display_name': '志工',
							},
							{
								'value': 'guest',
								'display_name': '視障者',
							},
						],
					},
					'subject': {
						'label': '主旨',
						'type': 'text',
					},
					'body': {
						'label': '內容',
						'type': 'textarea',
					},
				},
			}
		},
		metaInfo: {
			title: '訊息傳送',
		},
		mounted(){
		},
		methods: {
			send_email(){
				if(iser(this.category) | iser(this.subject) | iser(this.body)){
					alertmessage('error', '尚有欄位未填寫')
					return -1
				}

				let post_data = {
					'category': this.category,
					'subject': this.subject,
					'body': this.body,
				}

				genericUserAPI.userAction.email(post_data)
				.then(res => {
					alertmessage('success', '成功傳送訊息')
				})
				.catch(res => {
					alertmessage('error', o2j(res.response.data));
				})
			},
		},
	}
</script>