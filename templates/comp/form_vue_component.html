<template id="bs-form-group">
	<div class="form-horizontal">
		<template v-for="(detail, field) in model_infos">
			<div class="form-group">
				<label class="control-label col-sm-2" :for="field"><font style="color:red">*</font><span>{|{ detail.label }|}</span></label>
				<div class="col-sm-4">
					<input v-if="detail.type === 'text' || detail.type === 'email'" 
						maxlength="30"
						class="form-control" 
						:type="detail.type" 
						:id="field" 
						v-model="infos[field]"
					>

					<input v-if="detail.type === 'checkbox'" 
						:type="detail.type" 
						:id="field" 
						:checked="infos[field]"
						v-model="infos[field]"
					>

					<el-date-picker v-if="detail.type === 'date'" 
						v-model="infos[field]"
						:id="field"
						value-format="yyyy-MM-dd"   
						placeholder="yyyy-MM-dd"
						size=small
						style="width: 100%;"
					></el-date-picker>

					<select v-if="detail.type === 'select'"
						class="form-control"
						:id="field"
						v-model="infos[field]"
					>
						<template v-for="(name, val) in detail.choices">
							<option :value="val">{|{ name }|}</option>
						</template>
					</select>

					<template
						v-if="detail.type === 'radio'" 
						v-for="(name, val) in detail.choices"
					>
						<label class="radio-inline">
						<input 
							type="radio" 
							:id="field"
							:value="val"
							v-model="infos[field]" 
						> 
						{|{ name }|}
						</label>
					</template>
				</div>
				<label class="control-label col-sm-4" :for="field" style="text-align:left;"><font style="color:red">{|{ detail.remark }|}</font></label>
			</div>
		</template>
	</div>
</template>

<script>
	Vue.options.delimiters = ['{|{', '}|}'];

	Vue.component('form-component', {
		template: '#bs-form-group',
		props: ['model_infos', 'url', 'bus'],
		data: function(){
			return {
				infos: {},
				orig_infos: {},
			}
		},
		methods: {
			refresh_info: function() {
				this.infos = _.cloneDeep(this.orig_infos);
			},
			update_info: function() {
				let vo = this;
				rest_aj_send('patch', this.url, this.infos)
				.done(function(data, textStatus, xhr) {
					alertmessage('success', data['message'] +'更新已完成')
						.done(function () {
							location.reload(); //重新載入網頁以更新資訊
						});
				})
				.fail(function(data){
					alertmessage('error', data['message'])
					.done(function() {
						vo.refresh_info();
					})
				})
			},
		},
		created() {
			let vo = this;
			rest_aj_send('get', this.url, {})
			.done(function(data) {
				_.each(data.data, function(v, k){
					if(iser(v)) {
						// deal with undefined value
						data.data[k] = '';
					}
				});
				vo.infos = data.data;
				vo.orig_infos = _.cloneDeep(data.data); // back up
			})
		},
		mounted () {
			this.bus.$on('refresh', this.refresh_info);
			this.bus.$on('update', this.update_info);
		},
	});

</script>