<template id="bs-form-group">
	<div class="form-horizontal">
		<template v-for="item in fields">
			<div class="form-group">
				<label class="control-label col-sm-2" :for="'id_' +item.keys"><font style="color:red">*</font><span>{|{ item.model_info.label }|}</span></label>
				<div class="col-sm-4">
					<input
						v-if="item.model_info.type === 'text' || item.model_info.type === 'email' || item.model_info.type === 'checkbox'"
						class="form-control" 
						:type="item.model_info.type" 
						:id="'id_' +item.keys"
						v-model="new_datas[item.keys]"
					>

					<el-date-picker v-if="item.model_info.type === 'date'"
						:id="'id_' +item.keys"
						v-model="new_datas[item.keys]"
						value-format="yyyy-MM-dd"   
						placeholder="yyyy-MM-dd"
						size=small
						style="width: 100%;"
					></el-date-picker>

					<select v-if="item.model_info.type === 'select'"
						class="form-control"
						:id="'id_' +item.keys"
						v-model="new_datas[item.keys]"
					>
						<option
							v-for="option_item in item.model_info.choices"
							:value="option_item.value"
						>
							{|{ option_item.display_name }|}
						</option>
					</select>

					<template
						v-if="item.model_info.type === 'radio'" 
						v-for="option_item in item.model_info.choices"
					>
						<label class="radio-inline">
						<input 
							type="radio" 
							:id="'id_' +item.keys"
							:value="option_item.value"
						v-model="new_datas[item.keys]"
						> 
							{|{ option_item.display_name }|}
						</label>
					</template>
				</div>
				<label class="control-label col-sm-4" :for="'id_' +item.keys" style="text-align:left;"><font style="color:red">{|{ item.model_info.remark }|}</font></label>
			</div>
		</template>
	</div>
</template>

<script>
	Vue.options.delimiters = ['{|{', '}|}'];

	Vue.component('form-drf', {
		template: '#bs-form-group',
		props: ['fields', 'url', 'bus'],
		data: function(){
			return {
				new_datas: {},
				origin_datas: {},
			}
		},
		methods: {
			get: function() {
				this.$emit('get', this.new_datas)
			},
		},
		created: function() {
			let self = this;

			_.each(self.fields, function(v){
				self.origin_datas[v.keys] = v.value
			});
			self.new_datas = _.cloneDeep(self.origin_datas); // back up
		},
		mounted () {
			this.bus.$on('get', this.get);
		},
	});

</script>