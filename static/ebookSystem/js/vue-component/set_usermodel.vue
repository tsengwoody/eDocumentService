<template>
	<div>
		<div v-for="(model_info, key) in model_infos" :key="key">
			<form-drf
				:model_info="model_infos[key]"
				:input-class="'col-sm-4'"
				:field="key"
				:value="form[key]"
				v-model="form[key]"
			></form-drf>
		</div>
	</div>
</template>

<script>

	module.exports = {
		props: ['userdata'],
		components: {
			'form-drf': components['form'],
			// 'form-drf': httpVueLoader('/static/ebookSystem/js/vue-component/form.vue'),
		},
		data() {
			return {
				form: {
					email: '',
					first_name: '',
					last_name: '',
					phone: '',
					birthday: '',
					education: '',
					is_book: false,
					org: '',
				},
				model_infos: {
					'email': {
						'label': '信箱',
						'type': 'email',
						'remark': '請填寫電子信箱',
					},
					'first_name': {
						'label': '性氏',
						'type': 'text',
						'remark': '請填寫中文姓氏',
					},
					'last_name': {
						'label': '名字',
						'type': 'text',
						'remark': '請填寫中文名字',
					},
					'phone': {
						'label': '聯絡電話',
						'type': 'text',
						'remark': '請填寫手機',
					},
					'birthday': {
						'label': '生日',
						'type': 'date',
						'remark': '請填寫生日，範例日期格式：1989-02-19',
					},
					'education': {
						'label': '教育程度',
						'type': 'select',
						'remark': '請選擇教育程度',
						'choices': [
							{ display_name: '國小', value: '國小' },
							{ display_name: '國中', value: '國中' },
							{ display_name: '高中', value: '高中' },
							{ display_name: '學士', value: '學士' },
							{ display_name: '碩士', value: '碩士' },
						]
					},
					'is_book': {
						'label': '訂閱訊息',
						'type': 'checkbox',
						'remark': '訂閱訊息',
					},
					'org': {
						'label': '隸屬單位',
						'type': 'select',
						'remark': '請選擇所屬單位',
					},
				}
			}
		},
		mounted(){
			this.form = this.userdata;
		},
		methods: {
			updateUserInfo(userId){
				console.log(userId);
			},
		},
	};

</script>