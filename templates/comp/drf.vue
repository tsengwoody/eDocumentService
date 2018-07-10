<template id="drf-model">
	<div class="form-horizontal">
		<div class="form-group">
			<label
				:for="'id_' +keys"
				class="col-sm-3"
			>{|{ convertTitle[keys] }|}</label>
			<template v-if="mode==='read'">
				<div
					v-if="model_info.type==='choice' || model_info.type==='field'"
					class="col-sm-9"
				>{|{ value2display_name(value, model_info.choices) }|}</div>
				<div
					v-else
					class="col-sm-9"
				>{|{ value }|}</div>
			</template>
			<template v-if="mode==='write'">
				<input
					v-if="model_info.type==='string'"
					v-bind:value="value"
					v-on:input="$emit('input', $event.target.value)"
					v-bind:id="'id_' +keys"
					class="col-sm-9 form-control"
				>
				<select
					v-if="model_info.type==='choice' || model_info.type==='field'"
					v-bind:value="value"
					v-on:input="$emit('input', $event.target.value)"
					v-bind:id="'id_' +keys"
					class="col-sm-9 form-control"
				>
					<option
						v-for="item in model_info.choices"
						:value="item.value"
					>
						{|{ item.display_name }|}
					</option>
				</select>
				<el-date-picker
					v-if="model_info.type==='date'"
					v-bind:value="value"
					v-on:input="$emit('input', $event)"
					v-bind:id="'id_' +keys"
					value-format="yyyy-MM-dd"   
					placeholder="yyyy-MM-dd"
					size=small
					style="width: 100%;"
				></el-date-picker>
			</template>
		</div>
	</div>
</template>
<script>
	Vue.options.delimiters = ['{|{', '}|}'];

	Vue.component('drf-model', {
		template: '#drf-model',
		props: ['model_info', 'keys', 'value', 'mode',],
		methods: {
			value2display_name: function (value, choices) {
				display_name = value
				_.each(choices, function(v){
					if(v['value'] === value){
						display_name = v['display_name']
					}
				})
				return display_name
			},
		},
		created() {

		},
		mounted () {

		},
	})
</script>