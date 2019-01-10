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
			instance_set: function(pk){
				this.pk = pk
				this.get_priority()
			},
			get_priority: function(){
				let self = this
				rest_aj_send('get', '/ebookSystem/api/books/' +self.pk +'/action/set_priority/', {})
				.done(function (data) {
					self.priority = data['data'].priority
				})
				.fail(function(data){
					alertmessage('error', o2j(data))
				})
			},
			set_priority: function(){
				let self = this
				rest_aj_send('post', '/ebookSystem/api/books/' +self.pk +'/action/set_priority/', {'priority': self.priority})
				.done(function (data) {
					alertmessage('success', '成功設定權重')
						.done(function () {
							self.$emit('update')
						});
				})
				.fail(function(data){
					alertmessage('error', o2j(data))
				})
			},
		},
	};

</script>