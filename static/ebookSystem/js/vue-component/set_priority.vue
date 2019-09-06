<template>
	<div>
			<form-drf 
				:model_info="model_info.priority"
				:field="'priority'"
				:offset-class="'col-sm-offset-3'"
				v-model="priority"
				@keyup.enter.native="set_priority()"
			></form-drf>

	</div>
</template>

<script>

	module.exports = {
		components: {
			'form-drf': components['form'],
		},
		data: function(){
			return {
				pk: '',
				priority: '0',
				model_info: {
					'priority': {
						'label': '權重',
						'type': 'select',
						'choices' : [],
					},
				},
			}
		},
		mounted: function(){
			let self = this
			_.each([0, 1, 2, 3, 4, 5, 6, 7, 8, 9,], function(v){
				self.model_info.priority.choices.push({
					'value': v,
					'display_name': v,
				})
			})
		},
		methods: {
			instance_set(pk){
				this.pk = pk
				this.get_priority()
			},
			get_priority(){
				ebookSystemAPI.bookRest.read(this.pk)
				.then(res => {
					this.priority = res.data.priority;
				})
				.catch(res => {
					alertmessage('error', o2j(res.response.data));
				})
			},
			set_priority(){
				ebookSystemAPI.bookRest.partialupdate(this.pk, {priority: this.priority,})
				.then(res => {
					this.$emit('update')
					this.priority = res.data.priority;
					alertmessage('success', '成功設定權重')
				})
				.catch(res => {
					alertmessage('error', o2j(res.response.data));
				})
			},
		},
	};

</script>